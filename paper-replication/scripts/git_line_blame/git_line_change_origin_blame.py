git_path = '/home/lquerel/django'
    def create_commit_link(self, originating_commit, replaced_by_commit, line_count):
        cursor = self.db.cursor()
        cursor.execute("""INSERT INTO GIT_COMMIT_BLAME (ORIGIN, REPLACED_BY, LINE_COUNT) VALUES ('%s','%s',%s)""" %(originating_commit, replaced_by_commit, line_count))
        self.db.commit()

    command = "cd '%s'; git checkout -q master; git clean -f -d;  git checkout -q %s; git blame -L %s,%s -l -s %s" % (git_path, parent_commit_id, start, end, file_path)
    #print file_diff

    #diff_parts = re.findall("(@@.*\n(?:[+-].*\n)+)()", file_diff)
    #print diff_parts
    #for diff_part in diff_parts:
    #multi = re.findall("@@\s*-(\d+),(\d+)\s*\+\d+,(\d+)", file_diff)

    multi = re.findall("@@\s*-(\d+)(?:,)?(\d+|)", file_diff)
        start = multi[0]
        end = multi[len(multi)-1]
        change_line_start = int(start[0])-diff_history_size
        delta = (int(end[1])+diff_history_size-1) if end[1] else diff_history_size
        change_line_end = int(end[0])+delta

        print "Possible failure: parent commitid %s revision diff %s" % (parent_commit_id, file_diff)
        return {}
    #print "\nfile: %s \nstart line: %s\nend line: %s\nremoved: %s" % (file_path, change_line_start, change_line_end, lines_removed)
    if index_of_lines_removed != number_of_lines_removed:
        print "$$$$$$$$$$$$$$$$$$$$ MISMATCHED $$$$$$$$$$$$$$$$$$$$"
        parsed_revision = re.findall("a/(.+)\sb(.+\n){3,4}(@@\s+.+\s+@@.+(.*\n)*)*", revision)
            print "This should have been a revision, but was not flagged as one: %s" % revision
        if "new file mode" not in revision:
            commit_id_and_number_of_lines_affected = process_revision(parsed_revision, parent_commit_id)
        else:
            print "file: %s - new file" % parsed_revision[0][0]



    # manual_run = 26