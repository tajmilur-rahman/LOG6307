#!/usr/bin/python
import psycopg2
import datetime;
from datetime import date;
from settings.settings import *

conn = psycopg2.connect(database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, host=DATABASE_HOST, port="5432")
print "Opened database successfully"

_currYear = date.today().year

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
		cur.execute("select count(*) as exp, extract(year from c.author_dt) as year from git_commit c, git_revision r where c.commit=r.commit and c.author_dt < '"+str(author_date)+"' and c.author='"+str(author)+"' group by c.author, extract(year from c.author_dt) order by year desc")
		rExpRows = cur.fetchall()
		i = 1
		rexp = 0

		print "+-----------------------------------------------------+\n"
		for rExpRow in rExpRows :
			exp = rExpRow[0]
			year = int(rExpRow[1])
			print "| "+str(author)+" - "+str(int(year))+" - "+str(exp)+" |\n"
			rexp += (exp/i)
			i+=1
		print "+-----------------------------------------------------+\n"
		print "REXP: "+str(rexp)+"\n"
		cur.execute("update log6307_commit set rexp = "+str(rexp)+" where commit = '"+commit+"'")

conn.commit()
conn.close()
