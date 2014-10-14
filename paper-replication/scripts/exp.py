#!/usr/bin/python
##
# author: Md Tajmilur Rahman
# CESEL, Concordia University
# rupak.karmadhar@gmail.com

import psycopg2
import datetime;
from datetime import date;
from settings.settings import DATABASE_NAME, DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD

conn = psycopg2.connect(database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, host=DATABASE_HOST, port="5432")
print "Opened database successfully"

cur = conn.cursor()
cur.execute("select c1.commit, c1.author, c1.author_dt from git_commit c1, log6307_commit c2 where c1.commit=c2.commit")

if cur.rowcount > 0 :
	print "Total rows: ", cur.rowcount
	rows = cur.fetchall()
	for row in rows : # for each author check calculate REXP
		commit = row[0]
		author = row[1].replace("'", "")
		author_date = row[2]
		print commit+" - "+str(author)+" - "+str(author_date)+"\n"
		# Calculate experience for author
		cur.execute("select count(distinct c.commit) as exp from git_commit c, git_revision r where c.commit=r.commit and c.author_dt < '"+str(author_date)+"' and c.author='"+str(author)+"' group by c.author")
		expRows = cur.fetchall()
		for expRow in expRows :
			exp = expRow[0]
			print "EXP: "+str(exp)+"\n"
			cur.execute("update log6307_commit set exp = "+str(exp)+" where commit = '"+commit+"'")

conn.commit()
conn.close()
