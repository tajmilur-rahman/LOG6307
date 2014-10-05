from postgres import Postgres

__author__ = 'lquerel'


postgres = Postgres()

print "Finding commits which might have introduced bug based on commit which fixed it"

commits = postgres.get_fix_commits()

bug_commits = []

for commit in commits:

    fix_time = postgres.get_issue_reported_time_for_commit(commit)

    for bug in postgres.get_possible_bug_commits(commit, fix_time):
        if bug not in bug_commits:
            bug_commits.append(bug)

print "%s commits might have introduced bugs" % len(bug_commits)

print "Saving"

postgres.tag_bug_commits(bug_commits)

print "execution completed"
