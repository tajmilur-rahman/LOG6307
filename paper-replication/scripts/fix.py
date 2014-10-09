import logging
from settings.postgres import Postgres

__author__ = 'lquerel'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("entropy")

logger.info("Trying to find additional commits which fixed a bug")

postgres = Postgres()
postgres.find_other_fix_commits()
postgres.record_commit_issue_link_fix()

logger.info("Run complete")


