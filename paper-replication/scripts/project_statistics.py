__author__ = 'lquerel'

from settings.postgres import Postgres

statistics = {}

postgres = Postgres()

avg_file_changes = postgres.get_avg_number_file_changes()
statistics['total_commits'] = avg_file_changes[0]
statistics['files_per_change'] = avg_file_changes[1]

dates = postgres.get_start_and_end_of_development()
statistics['start_date'] = dates[0]
statistics['end_date'] = dates[1]
days = (dates[1] - dates[0]).days
statistics['changes_per_day'] = statistics['total_commits'] / float(days)
statistics['defect_commits_perc'] = float(postgres.get_number_defect_commits()[0])/float(statistics['total_commits'])
dev_statistics = postgres.get_dev_per_file_statistics()
statistics['max_dev_per_file'] = dev_statistics[0]
statistics['avg_dev_per_file'] = dev_statistics[1]

changes_loc_statistics = postgres.get_change_level_loc_statistics()
statistics['avg_loc_per_change'] = changes_loc_statistics[1]

print statistics
