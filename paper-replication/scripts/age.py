#!/usr/bin/python
import psycopg2
import datetime
import time
import calendar
import sys
from settings.settings import DATABASE_NAME, DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD

conn = psycopg2.connect(database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, host=DATABASE_HOST, port="5432");
print "Opened database successfully";

cur = conn.cursor();
cur.execute("select commit from log6307_commit");

conn.commit();
if cur.rowcount > 0 :
	print "Total rows: ", cur.rowcount;
	rows = cur.fetchall();
	for row in rows :
		commit = row[0];

		cur.execute("select canonical from git_revision where commit='"+str(commit)+"' and (add+remove)>0");
		if cur.rowcount > 0 :
			_files = cur.fetchall();
			for _file in _files :
				cur.execute("select author_dt from git_commit c, git_revision r where c.commit=r.commit and canonical='"+_file[0]+"' order by c.author_dt asc");
				if cur.rowcount > 0 :
					_authorDateRow = cur.fetchall();
					prevDate = _authorDateRow[0][0];
					i = sumDiff = avgDiff = 0;
					for _authorDate in _authorDateRow :
						#print _authorDate[0];
						currDate = _authorDate[0];
						if i>0 :
							d1 = calendar.timegm(time.strptime(prevDate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"));
							d2 = calendar.timegm(time.strptime(currDate.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"));
							diff = (d2-d1)/(24*60*60);
							sumDiff += diff;
						
						prevDate = currDate;
						i=i+1;
					
					avgDiff = sumDiff/i;
					cur.execute("update log6307_commit set age = '"+str(avgDiff)+"' where commit='"+str(commit)+"'");


conn.commit();
conn.close();
