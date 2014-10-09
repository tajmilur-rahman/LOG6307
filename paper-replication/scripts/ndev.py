#!/usr/bin/python
import psycopg2
from settings.settings import *

conn = psycopg2.connect(database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, host=DATABASE_HOST, port="5432")
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
				cur.execute("select count(distinct author) as numDevs from git_commit c, git_revision r where c.commit=r.commit and r.canonical = '"+_file[0]+"'");
				if cur.rowcount > 0 :
					_numDevRow = cur.fetchall();
					_numDevs = _numDevRow[0][0];

					f = open('ndev.rpt','w');
					f.write("commit  |  ndev\n");
					f.write(commit+" | "+str(_numDevs)+"\n"); # python will convert \n to os.linesep
					cur.execute("update log6307_commit set ndev = '"+str(_numDevs)+"' where commit='"+str(commit)+"'");

					
conn.commit();
				

f.close;
conn.close();
