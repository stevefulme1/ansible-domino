"""Poll Domino Data Lab for events."""

import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None


def _validate_host(host: str) -> bool:
    """Validate host parameter to prevent SSRF."""
    import re

    if "://" in host:
        logger.error(
            "Host parameter must not include a URL scheme (got '%s'). "
            "Provide only the hostname, e.g. 'app.dominodatalab.com'.",
            host,
        )
        return False

    if re.search(r'[/?#@]', host):
        logger.error("Host parameter contains invalid characters: %s", host)
        return False

    return True


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    """Poll Domino Data Lab API for events and push to EDA queue."""
    host = args["host"]

    if not _validate_host(host):
        logger.error("Host validation failed - event source will not start.")
        return

    interval = int(args.get("interval", 60))
    api_key = args.get("api_key", "")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    seen: set = set()

    while True:
        try:
            url = f"https://{host}/api/v1/events"
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            events = resp.json()
            if isinstance(events, dict):
                events = events.get("data", events.get("items", []))
            for event in events:
                event_id = event.get("id", "")
                if event_id and event_id not in seen:
                    seen.add(event_id)
                    await queue.put(event)
        except Exception as exc:
            logger.error("Error polling Domino Data Lab events: %s", exc)

        await asyncio.sleep(interval)


if __name__ == "__main__":

    class _MockQueue:
        async def put(self, item):
            print(item)

    asyncio.run(main(_MockQueue(), {"host": "app.dominodatalab.com", "interval": "10"}))
