from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import time


@dataclass
class IntakeRateLimitResult:
    allowed: bool
    retry_after_seconds: int


class IntakeRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, client_id: str, now: float | None = None) -> IntakeRateLimitResult:
        timestamp = now if now is not None else time.time()
        bucket = self._buckets[client_id]
        threshold = timestamp - self.window_seconds
        while bucket and bucket[0] <= threshold:
            bucket.popleft()
        if len(bucket) >= self.max_requests:
            retry_after = int(max(1, self.window_seconds - (timestamp - bucket[0])))
            return IntakeRateLimitResult(
                allowed=False,
                retry_after_seconds=retry_after,
            )
        bucket.append(timestamp)
        return IntakeRateLimitResult(allowed=True, retry_after_seconds=0)
