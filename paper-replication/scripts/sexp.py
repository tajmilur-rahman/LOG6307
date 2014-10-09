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
	rows = cur.fetchall()
	for row in rows : # for each author check calculate REXP
		commit = row[0]
		author = row[1].replace("'", "")
		author_date = row[2]
		#print commit+" - "+str(author)+" - "+str(author_date)+"\n"
		#print "select substring(canonical from E'^(.*?)\/') as s from git_revision where commit='"+commit+"'"
		cur.execute("select substring(canonical from E'^(.*?)\/') as s from git_revision where commit='"+commit+"'")
		if cur.rowcount > 0 :
			# current subsystems
			subsystemRows = cur.fetchall()
			s = ""
			for subsystems in subsystemRows :
				if (subsystems[0]  and len(subsystems[0]) > 0) : s = s+"'"+str(subsystems[0])+"',"
			s = s[:-1]
			if len and len(s) > 0 :
				print "select substring(canonical from E'^(.*?)\/') as s, count(distinct c.commit) as exp from git_commit c, git_revision r where c.commit=r.commit and c.author_dt < '"+str(author_date)+"' and c.author='"+str(author)+"' and substring(canonical from E'^(.*?)\/') in ("+s+") group by c.author, substring(canonical from E'^(.*?)\/')"
				cur.execute("select substring(canonical from E'^(.*?)\/') as s, count(distinct c.commit) as exp from git_commit c, git_revision r where c.commit=r.commit and c.author_dt < '"+str(author_date)+"' and c.author='"+str(author)+"' and substring(canonical from E'^(.*?)\/') in ("+s+") group by c.author, substring(canonical from E'^(.*?)\/')")
				sExpRows = cur.fetchall()
				i = 1
				sexp = 0
				#print "+-----------------------------------------------------+\n"
				for sExpRow in sExpRows :
					subsys = sExpRow[0]
					exp = sExpRow[1]
					print str(author)+" - "+subsys+" - "+str(exp)+"\n"
					sexp += exp
					i+=1
				#print "+-----------------------------------------------------+\n"
				print "SEXP: "+str(sexp)+"\n"
				cur.execute("update log6307_commit set sexp = "+str(sexp)+" where commit = '"+commit+"'")

conn.commit()
conn.close()
