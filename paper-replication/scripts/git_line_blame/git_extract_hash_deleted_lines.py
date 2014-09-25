import re
import psycopg2
from subprocess import call, check_output

__author__ = 'lquerel'

git_path = '/home/lquerel/Documents/MASTERS/LOG6307/6307 Assignment/django'
diff_history_size = 3


class Postgres:
    def __init__(self):

        host = "localhost"
        database_name = "assignment"
        username = "lquerel"
        password = "password"

        try:
            self.db = psycopg2.connect(
                "dbname='%s' user='%s' host='%s' password='%s'" % (database_name, username, host, password))
        except Exception as e:
            print "Failed to connect to database: %s" % e.message

    def get_commits(self):
        cursor = self.db.cursor()
        print "Obtaining list of commits"
        cursor.execute("""SELECT COMMIT, TREE, AUTHOR_DT, COMMITTER_DT FROM GIT_COMMIT""")
        print "Finished obtaining list of commits"
        commits = cursor.fetchall()
        return commits
        # self.db.commit()


"""
git log -p -1 c08c4fff40bae319cb8c4793ad8b11f7865a7dff

"""


def obtain_git_diff(git_path, commit_id):
    """
    Get the git diff

    :param git_path:
    :param commit_id:
    :return:
    """
    command = "cd '%s'; git log -p -1 %s" % (git_path, commit_id)
    return check_output(command, shell=True)

def obtain_git_blame(git_path, commit_id, file_path):
    command = "cd '%s'; git log -p -1 %s" % (git_path, commit_id)
    return check_output(command, shell=True)


postgres = Postgres()
commits = postgres.get_commits()


# Row format: ('commit', 'tree', 'author', author_dt, auth_id, 'committer', 'committer_dt, com_id, 'subject', num_child, num_parent, 'log')
commit_id = commits[0][0]  # Get the commit id
parent_commit_id = commits[0][1] # Id of parent commit
commit_diff = obtain_git_diff(git_path, commit_id)

# Split the commit diff into it's different files which were modified
revisions = re.split("diff --git", commit_diff)[1:]

# With the list of all file revisions from the commit diff we need to isolate it to each file revision
for revision in revisions:

    #result = re.search("a/.* b/(.*)\n((.*\n*)*)", revision)
    # result = re.findall("a(.+)(.+\n)+(@@\s+.+\s+@@.+(.*\n)*)*", revision)
    result = re.findall("a(.+)\sb(.+\n){4}(@@\s+.+\s+@@.+(.*\n)*)*", revision)
    if not result:
        print "This should have been a revision, but was not flagged as one: %s" % result
        # It seems that our revision is not actually a revision. We will skip it then
        continue
    else:
        # result as format ('file_path', '')('tests/migrations/test_state.py', 'index afd2f8b..ab65630 100644\n--- a/tests/m

        #file_path = result.group(0)
        #print result.groups() if result is not None else "no match"

        #re.finditer("")

        file_path = result[0][0]
        file_diff = result[0][2]

        ## diff_metrics eg. [('196', '7', '7')] [('a', 'b', 'c')]
        diff_metrics = re.findall("@@\s*-(\d+),(\d+)\s*\+\d+,(\d+)", file_diff)[0]
        change_line_start = diff_metrics[0]+diff_history_size
        change_line_end = diff_metrics[0]+diff_metrics[1]-diff_history_size

        lines_removed = re.findall("\n-(.*)", file_diff)

        obtain_git_blame(git_path, commit_id, file_path)

        print "%s - %s" % (file_path, file_diff)

"""
print commits[0]

command = "cd '/home/lquerel/Documents/MASTERS/LOG6307/6307 Assignment/django'; git show %s" % (commit_id)
print command
call(command, shell=True)
# call("cd '/home/lquerel/Documents/MASTERS/LOG6307/6307 Assignment/django'; git log", shell=True)

#call(["git", "status"], shell=True)
"""



