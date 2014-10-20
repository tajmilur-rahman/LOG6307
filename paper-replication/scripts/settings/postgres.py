import logging
import psycopg2
from settings import DATABASE_NAME, DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD

__author__ = 'lquerel'



class Postgres:
    def __init__(self):

        self.logger = logging.getLogger("Postgres")

        try:
            self.db = psycopg2.connect(
                "dbname='%s' user='%s' host='%s' password='%s'" % (DATABASE_NAME, DATABASE_USERNAME, DATABASE_HOST, DATABASE_PASSWORD))
        except Exception as e:
            print "Failed to connect to database: %s" % e.message

    def get_commits(self):
        cursor = self.db.cursor()
        logging.getLogger("Postgres")
        self.logger.info("Obtaining list of commits")
        cursor.execute("""SELECT GIT_COMMIT.COMMIT, GIT_DAG.PARENT FROM GIT_COMMIT, GIT_DAG WHERE GIT_COMMIT.COMMIT = GIT_DAG.CHILD""")
        self.logger.info("Finished obtaining list of commits")
        commits = cursor.fetchall()
        return commits
        # self.db.commit()

    def get_fix_commits(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT COMMIT FROM LOG6307_COMMIT WHERE FIX = TRUE""")
        return cursor.fetchall()

    def create_commit_link(self, originating_commit, replaced_by_commit, line_count):
        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO GIT_COMMIT_BLAME (ORIGIN, REPLACED_BY, LINE_COUNT) VALUES ('%s','%s',%s)""" %(originating_commit, replaced_by_commit, line_count))
        self.db.commit()

    def get_revisions_for_commit(self, commit_id):
        cursor = self.db.cursor()
        cursor.execute("""SELECT ADD, REMOVE FROM GIT_REVISION WHERE COMMIT = '%s'""" % commit_id)
        return cursor.fetchall()

    def add_entropy_and_lines_added_removed(self, commits):
        cursor = self.db.cursor()
        for commit_id in commits:
            commit = commits[commit_id]
            query = """UPDATE LOG6307_COMMIT SET LA = %s, LD = %s, ENTROPY = %s WHERE COMMIT = '%s'""" % (str(commit["added"]), str(commit["removed"]), str(commit["entropy"]), commit_id)

            cursor.execute(query)

        self.db.commit()

    def find_other_fix_commits(self):
        cursor = self.db.cursor()
        cursor.execute("""
        UPDATE LOG6307_COMMIT COMMIT SET FIX = TRUE FROM GIT_COMMIT GC
        WHERE GC.COMMIT = COMMIT.COMMIT AND(
        LOWER(GC.SUBJECT) like '%fix%' OR
        LOWER(GC.SUBJECT) like '%bug%' OR
        LOWER(GC.SUBJECT) like '%defect%' OR
        LOWER(GC.SUBJECT) like '%patch%' OR

        LOWER(GC.LOG) like '%fix%' OR
        LOWER(GC.LOG) like '%bug%' OR
        LOWER(GC.LOG) like '%defect%' OR
        LOWER(GC.LOG) like '%patch%')
        AND COMMIT.COMMIT NOT IN (SELECT COMMIT_ID FROM LOG6307_COMMIT_ISSUE_LINK)
        """)
        cursor.execute("""
        UPDATE LOG6307_COMMIT COMMITS SET FIX = TRUE FROM GIT_COMMIT AS GC, LOG6307_COMMIT_ISSUE_LINK AS LINK, LOG6307_ISSUES AS ISSUE

        WHERE COMMITS.COMMIT = GC.COMMIT AND
        (GC.COMMIT = LINK.COMMIT_ID AND LINK.ISSUE_ID = ISSUE.ID AND LOWER(ISSUE.TYPE) IN ('', 'uncategorized', NULL))

        AND (
        LOWER(GC.SUBJECT) like '%fix%' OR
        LOWER(GC.SUBJECT) like '%bug%' OR
        LOWER(GC.SUBJECT) like '%defect%' OR
        LOWER(GC.SUBJECT) like '%patch%' OR

        LOWER(GC.LOG) like '%fix%' OR
        LOWER(GC.LOG) like '%bug%' OR
        LOWER(GC.LOG) like '%defect%' OR
        LOWER(GC.LOG) like '%patch%');
        """)
        self.db.commit()

    def record_commit_issue_link_fix(self):
        cursor = self.db.cursor()
        cursor.execute("""
        UPDATE LOG6307_COMMIT COMMITS SET FIX = TRUE FROM LOG6307_COMMIT_ISSUE_LINK AS LINK, LOG6307_ISSUES AS ISSUE
        WHERE LOWER(ISSUE.TYPE) IN ('bug', 'defect', 'bug / defect', 'defaut')
        AND ISSUE.ID = LINK.ISSUE_ID
        AND LINK.COMMIT_ID = COMMITS.COMMIT """)
        self.db.commit()

    def get_issue_reported_time_for_commit(self, commit_id):
        cursor = self.db.cursor()
        query = """SELECT TIME FROM LOG6307_ISSUES ISSUES, LOG6307_COMMIT_ISSUE_LINK WHERE COMMIT_ID = '%s' AND ISSUE_ID = ISSUES.ID""" % commit_id
        #print query
        cursor.execute(query)
        return cursor.fetchall()

    def get_possible_bug_commits(self, commit_id, time):

        query = """SELECT ORIGIN FROM GIT_COMMIT_BLAME WHERE REPLACED_BY = '%s'""" % commit_id
        if not time and len(time) > 0:
            query = """SELECT ORIGIN FROM GIT_COMMIT_BLAME BLAME, GIT_COMMIT COMMIT WHERE BLAME.REPLACED_BY = '%s' AND COMMIT.AUTHOR_DT <= '%s'""" % (commit_id, time[0])
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def tag_bug_commits(self, commits):

        cursor = self.db.cursor()
        count = 1
        for commit in commits:
            print count
            count += 1
            cursor.execute("""UPDATE LOG6307_COMMIT COMMIT SET BUG = TRUE WHERE COMMIT.COMMIT = '%s'""" % commit)

        self.db.commit()

    def get_number_defect_commits(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT COUNT(COMMIT) FROM LOG6307_COMMIT WHERE BUG = TRUE""")
        return cursor.fetchone()

    def get_start_and_end_of_development(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT MIN(AUTHOR_DT), MAX(AUTHOR_DT) FROM GIT_COMMIT""")
        return cursor.fetchone()

    def get_avg_number_file_changes(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT COUNT(COMMITS) AS COMMITS, AVG(FILES) AS AVG_CHANGE FROM
            (SELECT COMMIT AS COMMITS, COUNT(CANONICAL) AS FILES FROM GIT_REVISION GROUP BY COMMIT) AS REVISIONS""")
        return cursor.fetchone()

    def get_dev_per_file_statistics(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT MAX(AUTHOR_COUNT), AVG(AUTHOR_COUNT) FROM
            (SELECT CANONICAL, COUNT(DISTINCT(AUTHOR)) AS AUTHOR_COUNT
            FROM GIT_COMMIT AS COMMIT, GIT_REVISION AS REVISION
            WHERE COMMIT.COMMIT = REVISION.COMMIT GROUP BY CANONICAL) AS DEV_COUNT""")
        return cursor.fetchone()

    def get_change_level_loc_statistics(self):
        cursor = self.db.cursor()
        cursor.execute("""SELECT COUNT(COMMIT) AS COMMITS, AVG(LINES) AS AVG_LINES FROM
            (SELECT COMMIT, SUM(ADD) + SUM(REMOVE) AS LINES FROM GIT_REVISION GROUP BY COMMIT) AS LINES_STAT""")
        return cursor.fetchone()

    def get_avg_file_level_loc_statistics(self):
        cursor = self.db.cursor()
        cursor.execute(""" """)

    def get_all_metrics(self):
        cursor = self.db.cursor()
        query = """SELECT * FROM LOG6307_COMMIT"""
        cursor.execute(query)
        return cursor.fetchall()
