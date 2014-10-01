#!/usr/bin/python
import psycopg2
import datetime;
from datetime import date;

conn = psycopg2.connect(database="assignment", user="rupak", password="karmadharRL-32", host="127.0.0.1", port="5432")
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
		cur.execute("select sum(add+remove) as churn from git_commit c, git_revision r where c.commit=r.commit and c.author_dt < '"+str(author_date)+"' and c.author='"+str(author)+"' group by c.author")
		expRows = cur.fetchall()
		for expRow in expRows :
			exp = expRow[0]
			print "EXP: "+str(exp)+"\n"
			cur.execute("update log6307_commit set exp = "+str(exp)+" where commit = '"+commit+"'")

conn.commit()
conn.close()
