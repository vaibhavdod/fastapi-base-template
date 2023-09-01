import logging

from core.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def init() -> None:
    """
        Based on the environment where this is triggered from
        We can create more details data required from our use cases
        Things to consider for init db would be:
        1. Super USer
        2. Meta data
        3. Config driven DB set up 
        4. testing data insertion
        5. and so on
    """
    db = SessionLocal()
    # 
    # 

def main() -> None:
    log.info("Creating initial data")
    init()
    log.info("Initial data created")


if __name__ == "__main__":
    main()
