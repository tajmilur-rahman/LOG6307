from decimal import Decimal
from settings.postgres import Postgres
import logging

__author__ = 'lquerel'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("entropy")

logger.info("Entropy, lines added and removed calculation")

postgres = Postgres()

commits = postgres.get_commits()
logger.info("Commits obtained. Need to process %s commits" % len(commits))

processed_commits = {}

count = 0
for commit_id, parent_id in commits:
    logging.debug(commit_id)
    count += 1

    revisions = postgres.get_revisions_for_commit(commit_id)

    lines_added = 0
    lines_removed = 0

    entropy_equation = ""

    for revision in revisions:
        added = revision[0]
        lines_added += added if added is not None and isinstance(added, Decimal) else 0

        removed = revision[1]
        lines_removed += removed if removed is not None and isinstance(removed, Decimal) else 0

        if added and removed:
            revision_total = added + removed
            if revision_total > 0:
                entropy_equation += "-(%s/float(total_lines))*log((%s/float(total_lines)),2)" % (revision_total, revision_total)
            logging.debug("%s %s : %s" % (added, removed, entropy_equation))

    total_lines = lines_added + lines_removed

    entropy = eval(entropy_equation) if entropy_equation != "" else 0
    logger.info("Commit %s: %s=%s" % (commit_id, entropy_equation, entropy))

    processed_commits[commit_id] = {"added": lines_added, "removed": lines_removed, "entropy": abs(entropy)}

postgres.add_entropy_and_lines_added_removed(processed_commits)
logging.info("Finished processing lines added, removed and commit entropy")