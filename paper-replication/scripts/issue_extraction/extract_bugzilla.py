import csv
import os
import logging
from pymongo import MongoClient
import psycopg2

__author__ = 'lquerel'


"""
Used to extract issues from tsv
"""


class Mongo:

    def __init__(self):
        logging.getLogger("mongo")
        client = MongoClient()
        logging.info("Created mongo client")
        self.db = client.assignment_6307
        logging.info("Getting access to db")
        self.bugzilla = self.db.bugzilla
        logging.info("Getting access to collection")

    def add_report(self, row_values):

        #bugzilla_report = {"id": id, "summary": summary, "status": status, "owner": owner, "type": type, "component": component, "version": version}

        object = self.bugzilla.insert(row_values)

        logging.info("Object in mongo: %s" % object)


class Postgres:

    def __init__(self):

        host = "localhost"
        database_name = "assignment"
        username = "lquerel"
        password = "password"

        try:
            self.db = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (database_name, username, host, password))
        except Exception as e:
            print "Failed to connect to database: %s" % e.message


    def insert_bugzilla_issues(self, issues):
        cursor = self.db.cursor()
        print "Generating postgres query"
        cursor.executemany("""INSERT INTO LOG6307_ISSUES(id, summary, owner, type, status, version, component) VALUES
                            (%(id)s, %(summary)s, %(owner)s, %(type)s, %(status)s, %(version)s, %(component)s)""", issues)
        print "Committing to postgres"
        self.db.commit()



print os.path.dirname("Running script from: %s" % os.path.abspath(__file__))
csv_file_name = "bug_tracker.tsv"
csv_file = open(csv_file_name, 'rb')
reader = csv.reader(csv_file, delimiter='\t')

mongo = Mongo()
postgres = Postgres()

first_row = reader.next()
issues = []

for row in reader:
    row_value = {}
    for index in range(len(first_row)):
        # Take the column headings and apply them to each row. Replace '' values with None
        row_value[first_row[index]] = row[index] if row[index] != '' else None
    issues.append(row_value)

postgres.insert_bugzilla_issues(tuple(issues))


