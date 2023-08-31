"""
This script is used to check if the database is awake and ready to accept connections.
"""

import asyncio
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import logging
from sqlalchemy import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from core.db import SessionLocal

logging.basicConfig(level=logging.DEBUG, handlers=[
    logging.StreamHandler(sys.stdout)
])
log = logging.getLogger(__name__)



max_tries = 60 * 5  # 5 minutes
wait_seconds = 1




@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(log, logging.INFO),
    after=after_log(log, logging.WARN),
)
def init() -> None:
    try:
        # Try to create session to check if DB is awake
        query = select(1)
        session = SessionLocal()
        session.execute(query)
    except Exception as e:
        log.error(e)
        raise e


def main() -> None:
    log.info("Initializing service")
    init()
    log.info("Service finished initializing")


if __name__ == "__main__":
   main()