import re
import psycopg2
from subprocess import call, check_output

__author__ = 'lquerel'

git_path = '/home/lquerel/Documents/MASTERS/LOG6307/6307 Assignment/django'
diff_history_size = 0


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
        cursor.execute("""SELECT GIT_COMMIT.COMMIT, GIT_DAG.PARENT FROM GIT_COMMIT, GIT_DAG WHERE GIT_COMMIT.COMMIT = GIT_DAG.CHILD""")
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
    command = "cd '%s'; git log -U%s -p -1 %s" % (git_path, diff_history_size, commit_id)
    return check_output(command, shell=True)


def obtain_git_blame(git_path, parent_commit_id, file_path, start, end):
    command = "cd '%s'; git checkout -q master;  git checkout -q %s; git blame -L %s,%s -l -s %s" % (git_path, parent_commit_id, start, end, file_path)
    return check_output(command, shell=True)
    # (\w\d)+\s+(\d+)\)(.*)


def process_revision(revision):
    # revision as format ('file_path', '')('tests/migrations/test_state.py', 'index afd2f8b..ab65630 100644\n--- a/tests/m

    file_path = revision[0][0]
    file_diff = revision[0][2]

    ## diff_metrics eg. [('196', '7', '7')] [('a', 'b', 'c')]
    diff_metrics = re.findall("@@\s*-(\d+),(\d+)\s*\+\d+,(\d+)", file_diff)[0]
    change_line_start = int(diff_metrics[0])+diff_history_size
    change_line_end = int(diff_metrics[0])+int(diff_metrics[1])-diff_history_size-1

    lines_removed = re.findall("\n-(.*)", file_diff)
    number_of_lines_removed = len(lines_removed)


    print "\nfile: %s \nstart line: %s\nend line: %s\nremoved: %s" % (file_path, change_line_start, change_line_end, lines_removed)
    git_blame = obtain_git_blame(git_path, parent_commit_id, file_path, change_line_start, change_line_end).split("\n")


    index_of_lines_removed = 0
    commit_origin_of_removed_lines = {}

    if number_of_lines_removed > 0:
        for i in range(len(git_blame)):
            print "loop"+str(i)
            if index_of_lines_removed >= number_of_lines_removed:
                # all lines have been found
                print "No more lines to match to revision"
                break

            if lines_removed[index_of_lines_removed] in git_blame[i]:
                # We could keep track of the line number change_line_start+i
                line_commit_id = git_blame[index_of_lines_removed][:40]
                if line_commit_id in commit_origin_of_removed_lines:
                    commit_origin_of_removed_lines[line_commit_id] += 1
                else:
                    commit_origin_of_removed_lines[line_commit_id] = 1
                index_of_lines_removed += 1


    return commit_origin_of_removed_lines

def process_commit():
    global commit_diff, revisions, commit_origin_of_removed_lines, revision, parsed_revision, commit_id_and_number_of_lines_affected, prev_commit_id
    print "Parent: %s, Commit: %s" % (parent_commit_id, commit_id)
    commit_diff = obtain_git_diff(git_path, commit_id)
    # Split the commit diff into it's different files which were modified
    revisions = re.split("diff --git", commit_diff)[1:]
    print revisions
    commit_origin_of_removed_lines = {}
    # With the list of all file revisions from the commit diff we need to isolate it to each file revision
    for revision in revisions:
        parsed_revision = re.findall("a/(.+)\sb(.+\n){4}(@@\s+.+\s+@@.+(.*\n)*)*", revision)
        if not parsed_revision:
            print "This should have been a revision, but was not flagged as one: %s" % parsed_revision
            # It seems that our revision is not actually a revision. We will skip it then
            continue

        commit_id_and_number_of_lines_affected = process_revision(parsed_revision)

        for prev_commit_id in commit_id_and_number_of_lines_affected.keys():
            if prev_commit_id in commit_origin_of_removed_lines:
                commit_origin_of_removed_lines[prev_commit_id] += commit_id_and_number_of_lines_affected[prev_commit_id]
            else:
                commit_origin_of_removed_lines[prev_commit_id] = commit_id_and_number_of_lines_affected[prev_commit_id]
    print "Commmits which had lines which were removed by current commit: %s" % commit_origin_of_removed_lines


postgres = Postgres()
commits = postgres.get_commits()


# Row format: ('commit', 'tree', 'author', author_dt, auth_id, 'committer', 'committer_dt, com_id, 'subject', num_child, num_parent, 'log')
commit_id = commits[0][0]  # Get the commit id
parent_commit_id = commits[0][1] # Id of parent commit

for index in range(1):
    process_commit()
