#!/usr/bin/python
import psycopg2

conn = psycopg2.connect(database="assignment", user="rupak", password="karmadharRL-32", host="127.0.0.1", port="5432")
print "Opened database successfully"

cur = conn.cursor()
cur.execute("select c1.commit, c1.author_dt from git_commit c1, log6307_commit c2 where c1.commit=c2.commit")

if cur.rowcount > 0 :
	print "Total rows: ", cur.rowcount
	rows = cur.fetchall()
	for row in rows :
		commit = row[0]
		author_date = row[1]
		#print commit+" - "+str(author_date)+"\n"
		cur.execute("select canonical from git_revision where commit='"+str(commit)+"' and (add+remove)>0")
		if cur.rowcount > 0 :
			_files = cur.fetchall()
			l = []
			for _file in _files :
				cur.execute("select c.commit from git_commit c, git_revision r where canonical='"+_file[0]+"' and c.author_dt < '"+str(author_date)+"' order by c.author_dt desc")
				if cur.rowcount > 0 :
					_prevChanges = cur.fetchall()
					l.append(_prevChanges[0][0])
			if len(l) > 0 : l = set(l)
			nuc = len(l)
			print str(nuc)+"\n"
			cur.execute("update log6307_commit set nuc = "+str(nuc)+" where commit = '"+commit+"'")
conn.commit()
conn.close()
