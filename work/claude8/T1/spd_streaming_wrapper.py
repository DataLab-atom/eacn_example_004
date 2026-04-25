"""
Streaming SPD wrapper — SpilledTermsDict for SPD memory-bounded execution.

Background
----------
claude4's spd_otoc_core.py uses a `Dict[Tuple[int,...], complex]` to hold all
Pauli terms during Heisenberg evolution. On 16q+ scrambled OTOC^(2), this dict
overflows 8 GB RAM mid-evolution (claude4 commit a6b1697 / msg ~tick #44).

This wrapper provides a `SpilledTermsDict` that implements the MutableMapping
protocol (drop-in for `dict`) but maintains a two-tier storage:

  - **RAM tier**: an LRU `OrderedDict` capped at `ram_capacity` entries.
    All recently-touched keys live here. Conjugation can read/write at full speed.
  - **Disk tier**: a single sqlite database that holds the rest.
    Spilled keys live here keyed by their bytes-encoded tuple representation.

On `__setitem__`, if the key has |c|^2 < spill_threshold, it goes straight to
disk; otherwise it lands in RAM. When RAM exceeds `ram_capacity`, the LRU
oldest entries are spilled to disk in batch.

This is INSTRUMENTATION not REIMPLEMENTATION (per claude4 ack of differentiation
boundary): claude4's SPD evolution code is unchanged — only `PauliOperator.terms`
is replaced via injection.

Schema (per claude4 ack)
------------------------
- key: ``Tuple[int, ...]`` of {0, 1, 2, 3} — Pauli string indices
- value: ``complex`` coefficient
- methods used by spd_otoc_core: ``__getitem__``, ``__setitem__``, ``__iter__``,
  ``items()``, ``get(key, default)``

Usage (when injected into spd_otoc_core)
----------------------------------------
    from work.claude8.T1.spd_streaming_wrapper import SpilledTermsDict
    pauli_op.terms = SpilledTermsDict(
        ram_capacity=1_000_000,
        spill_threshold=1e-12,
        db_path="streaming_terms.db",
    )

Author: claude8 (branch claude8)
Status: prototype + smoke test
"""

from __future__ import annotations

import math
import os
import pickle
import sqlite3
import tempfile
from collections import OrderedDict
from collections.abc import MutableMapping
from typing import Any, Iterator, Optional


_SENTINEL = object()


class SpilledTermsDict(MutableMapping):
    """
    Disk-spilled MutableMapping with LRU RAM tier.

    Parameters
    ----------
    ram_capacity : int
        Max number of (key, complex) entries kept in the RAM LRU. Once exceeded,
        the oldest entries are flushed to the sqlite tier.
    spill_threshold : float
        Items with |value|^2 strictly below this go to disk on insert (bypassing
        RAM). 0.0 disables eager-spill (everything starts in RAM).
    db_path : str | None
        Path for the sqlite file. None => a temp file in the system tempdir,
        cleaned up on close().
    flush_batch : int
        How many oldest LRU entries to flush at once when RAM exceeds capacity.
        Larger batches amortise sqlite I/O.
    """

    def __init__(
        self,
        ram_capacity: int = 1_000_000,
        spill_threshold: float = 1e-12,
        db_path: Optional[str] = None,
        flush_batch: int = 4096,
    ) -> None:
        if ram_capacity <= 0:
            raise ValueError("ram_capacity must be positive")
        if spill_threshold < 0:
            raise ValueError("spill_threshold must be >= 0")
        if flush_batch <= 0:
            raise ValueError("flush_batch must be positive")
        self._ram: "OrderedDict[tuple, complex]" = OrderedDict()
        self._ram_capacity = ram_capacity
        self._spill_threshold = spill_threshold
        self._flush_batch = flush_batch
        self._owns_db = db_path is None
        if self._owns_db:
            fd, db_path = tempfile.mkstemp(prefix="spd_streaming_", suffix=".db")
            os.close(fd)
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS terms (k BLOB PRIMARY KEY, v BLOB NOT NULL)"
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._conn.commit()
        self._disk_count = self._count_disk()
        self._spilled_total = 0
        self._reloaded_total = 0

    # ---- core MutableMapping API ----

    def __getitem__(self, key: tuple) -> complex:
        # Invariant: a key lives in exactly one tier at a time.
        if key in self._ram:
            self._ram.move_to_end(key)
            return self._ram[key]
        v = self._fetch_disk(key)
        if v is _SENTINEL:
            raise KeyError(key)
        self._reloaded_total += 1
        # Promote on read: pull from disk to RAM, then DELETE the disk copy
        # so the invariant holds.
        self._delete_disk(key)
        self._ram[key] = v  # type: ignore[assignment]
        self._ram.move_to_end(key)
        self._evict_if_needed()
        return v  # type: ignore[return-value]

    def __setitem__(self, key: tuple, value: complex) -> None:
        amp_sq = (value.real * value.real) + (value.imag * value.imag)
        if amp_sq < self._spill_threshold:
            # Eager-spill: bypass RAM entirely, evict from RAM if present.
            if key in self._ram:
                del self._ram[key]
            self._write_disk(key, value)
            return
        # Above threshold → goes to RAM. Ensure no stale disk copy.
        if key in self._ram:
            self._ram[key] = value
            self._ram.move_to_end(key)
            return
        # Was the key previously on disk? Delete the stale disk copy so the
        # invariant (RAM ⊕ disk) holds.
        self._delete_disk(key)
        self._ram[key] = value
        self._evict_if_needed()

    def __delitem__(self, key: tuple) -> None:
        had = False
        if key in self._ram:
            del self._ram[key]
            had = True
        cur = self._conn.execute("DELETE FROM terms WHERE k = ?", (self._encode_key(key),))
        if cur.rowcount > 0:
            self._disk_count -= 1
            self._conn.commit()
            had = True
        if not had:
            raise KeyError(key)

    def __iter__(self) -> Iterator[tuple]:
        seen = set()
        for k in self._ram:
            seen.add(k)
            yield k
        for (kbytes,) in self._conn.execute("SELECT k FROM terms"):
            k = self._decode_key(kbytes)
            if k not in seen:
                yield k

    def __len__(self) -> int:
        # Disk and RAM never overlap with the same key (we always either-or),
        # so simple sum is correct.
        return len(self._ram) + self._disk_count

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, tuple):
            return False
        if key in self._ram:
            return True
        return self._fetch_disk(key) is not _SENTINEL

    # ---- helpers ----

    def get(self, key: tuple, default: Any = None) -> Any:  # type: ignore[override]
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):  # type: ignore[override]
        for k in self:
            yield k, self[k]

    def telemetry(self) -> dict:
        return {
            "ram_size": len(self._ram),
            "disk_size": self._disk_count,
            "spilled_total": self._spilled_total,
            "reloaded_total": self._reloaded_total,
            "db_path": self._db_path,
        }

    def close(self) -> None:
        try:
            self._conn.close()
        finally:
            if self._owns_db and os.path.exists(self._db_path):
                os.remove(self._db_path)

    # ---- internal disk routines ----

    @staticmethod
    def _encode_key(key: tuple) -> bytes:
        return pickle.dumps(key, protocol=4)

    @staticmethod
    def _decode_key(b: bytes) -> tuple:
        return pickle.loads(b)

    @staticmethod
    def _encode_value(v: complex) -> bytes:
        return pickle.dumps(v, protocol=4)

    @staticmethod
    def _decode_value(b: bytes) -> complex:
        return pickle.loads(b)

    def _count_disk(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM terms")
        return int(cur.fetchone()[0])

    def _fetch_disk(self, key: tuple):
        row = self._conn.execute(
            "SELECT v FROM terms WHERE k = ?", (self._encode_key(key),)
        ).fetchone()
        if row is None:
            return _SENTINEL
        return self._decode_value(row[0])

    def _write_disk(self, key: tuple, value: complex) -> None:
        # INSERT OR REPLACE — count update only on insert.
        kbytes = self._encode_key(key)
        existing = self._conn.execute(
            "SELECT 1 FROM terms WHERE k = ?", (kbytes,)
        ).fetchone()
        self._conn.execute(
            "INSERT OR REPLACE INTO terms VALUES (?, ?)",
            (kbytes, self._encode_value(value)),
        )
        if existing is None:
            self._disk_count += 1
        self._conn.commit()

    def _delete_disk(self, key: tuple) -> bool:
        """Remove a key from the disk tier if present. Returns True if deleted."""
        cur = self._conn.execute(
            "DELETE FROM terms WHERE k = ?", (self._encode_key(key),)
        )
        if cur.rowcount > 0:
            self._disk_count -= 1
            self._conn.commit()
            return True
        return False

    def _evict_if_needed(self) -> None:
        excess = len(self._ram) - self._ram_capacity
        if excess <= 0:
            return
        flush = max(excess, self._flush_batch)
        flushed = []
        for _ in range(flush):
            if not self._ram:
                break
            k, v = self._ram.popitem(last=False)
            flushed.append((self._encode_key(k), self._encode_value(v)))
        if not flushed:
            return
        # Bulk insert into disk tier.
        new_count = 0
        cur = self._conn.cursor()
        for kbytes, vbytes in flushed:
            existing = cur.execute(
                "SELECT 1 FROM terms WHERE k = ?", (kbytes,)
            ).fetchone()
            cur.execute(
                "INSERT OR REPLACE INTO terms VALUES (?, ?)", (kbytes, vbytes)
            )
            if existing is None:
                new_count += 1
        self._conn.commit()
        self._disk_count += new_count
        self._spilled_total += len(flushed)


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def _smoke():
    d = SpilledTermsDict(ram_capacity=4, spill_threshold=1e-9, flush_batch=2)
    try:
        # Insert above-threshold entries: live in RAM.
        d[(0, 0, 0)] = complex(0.5)
        d[(0, 1, 0)] = complex(0.3)
        assert d.telemetry()["ram_size"] == 2
        assert d.telemetry()["disk_size"] == 0

        # Eager-spill (very small amplitude).
        d[(1, 1, 1)] = complex(1e-6)
        # |1e-6|^2 = 1e-12 < 1e-9, so it should go to disk.
        # NOTE: we fixed the threshold semantics to compare amp_sq < spill,
        # so 1e-12 < 1e-9 is True → eager-spill expected.
        tel = d.telemetry()
        assert tel["disk_size"] == 1, f"expected 1 disk entry, got {tel['disk_size']}"
        assert (1, 1, 1) in d
        assert d[(1, 1, 1)] == complex(1e-6)

        # Trigger LRU evict by overflowing ram_capacity.
        for i in range(6):
            d[(2, i, 0)] = complex(1.0 + 0.1 * i)
        # ram_capacity = 4 → at least 2-3 entries should have spilled.
        tel = d.telemetry()
        assert tel["ram_size"] <= 4
        assert tel["spilled_total"] >= 2

        # Make sure all keys still readable across tiers.
        assert math.isclose(d[(0, 0, 0)].real, 0.5)
        assert math.isclose(d[(2, 5, 0)].real, 1.5)

        # Iteration covers all keys (no duplicates).
        keys = list(d)
        assert len(set(keys)) == len(keys)
        assert len(keys) == len(d)

        # Length includes both tiers.
        assert len(d) == tel["ram_size"] + tel["disk_size"]

        # Delete works across tiers.
        del d[(1, 1, 1)]
        assert (1, 1, 1) not in d

        print(f"smoke OK — {d.telemetry()}")
    finally:
        d.close()


if __name__ == "__main__":
    _smoke()
