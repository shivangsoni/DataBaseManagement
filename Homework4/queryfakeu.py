import os
import psycopg2
import csv
import glob
import sys

conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()

def prob3a():
	print("Executing 3A Code:\n")
	for i in range(1, 21):
		cur.execute("""
		select ((count(studentsTakeUnits.SID) + 0.00) / uniqueStudentSIDS.total * 100) AS Answer
		from (select Term, SID, SUM(Units) as totalUnits
			from (coursestudent natural join CourseAdministrative) AS combo
			where combo.Subj = 'ABC' OR combo.Subj = 'DEF'
			GROUP BY Term, SID
			) AS studentsTakeUnits,
			(select count(distinct SID) AS total
				from student
			) AS uniqueStudentSIDS
		where totalUnits = """ + str(i) + """
		GROUP BY total;
		""")
		result = cur.fetchone()
		print("Percentage of students that attempted " + str(i) + " units: " +  str(int(result[0] * 100) / 100.0) + "%\n")
      
def prob3b():
	print("Executing 3B Code:\n")
	cur.execute(""" 
	alter table coursestudent add column points float;
	""")

	cur.execute("""
	update coursestudent set points = 4.0 where grade = 'A+';
	""")
	
	cur.execute("""
	update coursestudent set points = 4.0 where grade = 'A';
	""")
	
	cur.execute("""
	update coursestudent set points = 3.7 where grade = 'A-';
	""")
	
	cur.execute("""
	update coursestudent set points = 3.3 where grade = 'B+';
	""")
	
	cur.execute("""
	update coursestudent set points = 3.0 where grade = 'B';
	""")
	
	cur.execute("""
	update coursestudent set points = 2.7 where grade = 'B-';
	""")
	
	cur.execute("""
	update coursestudent set points = 2.3 where grade = 'C+';
	""")
	
	cur.execute("""
	update coursestudent set points = 2.0 where grade = 'C';
	""")
	
	cur.execute("""
	update coursestudent set points = 1.7 where grade = 'C-';
	""")
	
	cur.execute("""
	update coursestudent set points = 1.3 where grade = 'D+';
	""")
	
	cur.execute("""
	update coursestudent set points = 1.0 where grade = 'D';
	""")
	
	cur.execute("""
	update coursestudent set points = 0.7 where grade = 'D-';
	""")
	
	cur.execute("""
	update coursestudent set points = 0.0 where grade = 'F';
	""")
	
	cur.execute("""
	update coursestudent set points = 0.0 where grade = 'I';
	""")
	
	cur.execute("""
	select instructor,D.net from (select instructor,AVG(points) as net from meeting,(select cid,term,grade,points from coursestudent) AS T where T.cid = meeting.cid and T.term = meeting.term and grade != 'P' and grade != 'NP' and grade !='S' and grade != 'NS' group by instructor) as D where D.net in (select max(net) from (select instructor,AVG(points) as net from meeting,(select cid,term,grade,points from coursestudent) AS T where T.cid = meeting.cid and T.term = meeting.term and grade != 'P' and grade != 'NP' and grade !='S' and grade != 'NS'  and grade != 'WD2' and grade != 'W04' and grade!= 'NG' and grade != 'WDC' and grade != 'WD1' and grade!= 'WN' and grade!='IP' group by instructor) as D);
	""")

	result = cur.fetchone()
	while result is not None:
	  print("Instructor with easy marking "+str(result))
	  result = cur.fetchone()

	cur.execute("""
	select instructor,D.net from (select instructor,AVG(points) as net from meeting,(select cid,term,grade,points from coursestudent) AS T where T.cid = meeting.cid and T.term = meeting.term and grade != 'P' and grade != 'NP' and grade !='S' and grade != 'NS' group by instructor) as D where D.net in (select min(net) from (select instructor,AVG(points) as net from meeting,(select cid,term,grade,points from coursestudent) AS T where T.cid = meeting.cid and T.term = meeting.term and grade != 'P' and grade != 'NP' and grade !='S' and grade != 'NS'  and grade != 'WD2' and grade != 'W04' and grade!= 'NG' and grade != 'WDC' and grade != 'WD1' and grade!= 'WN' and grade!='IP' group by instructor) as D);
	""")


	result = cur.fetchone()
	while result is not None:
	  print("Instructor with difficult marking "+str(result))
	  result = cur.fetchone()

	cur.execute(""" 
	alter table coursestudent drop column points;
	""")
	print("\n")

def prob3c():
	print("Executing 3C Code:\n")
	AverageGPA = []
   	totalNumStudentsEachUnit = []
   	tables = set([])
   	cur.execute("SELECT table_name from information_schema.tables where table_schema = 'public'")
   	tableNames = cur.fetchall()
   
   	for i in range(1, len(tableNames) + 1):
	   	tables.add(str(tableNames[i - 1][0]))
      
   	if "gpa" not in  tables:
		cur.execute("CREATE TABLE GPA (Grade varchar(2), Points float);")
		cur.execute("""INSERT INTO GPA VALUES 
		('A+', 4.0),('A', 4.0),('A-', 3.7),
		('B+', 3.3),('B', 3.0),('B-', 2.7),
		('C+', 2.3),('C', 2.0),('C-', 1.7),
		('D+', 1.3),('D', 1.0),('D-', 0.7),
		('F', 0.0);
		""")

	for i in range(1, 21):
		cur.execute("""
		select AVG(Points) as Answer
		from ((select SID, Term
			from (select SID, Term, SUM(Units) as totalUnitsPerTerm
				from (select SID, Term, Units
					from (coursestudent natural join (select CID, Term, Subj
									from courseadministrative
									where Subj = 'ABC' OR Subj = 'DEF') AS courseCTS
						)) AS InfoSTU
			GROUP BY SID, Term, Units) AS studentSTS
			where studentSTS.totalUnitsPerTerm = """ + str(i) + """
			) AS studentST
			natural join
	     		(select SID, Term, Grade, Points
				from coursestudent natural join gpa
				where Grade IS NOT NULL
				) AS studentSTGP
			) AS result;
		""")
		result = cur.fetchone()
		print("Average GPA of students taking " + str(i) + " units: " + str(result[0]) + "\n")
   
def prob3d():
	print("Executing 3D Code:\n")
   	cur.execute(""" 
   	alter table coursestudent add column points float;
   	""")
   
   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'A+';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'A';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'A-';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'B+';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'B';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'B-';
   	""")
	
	cur.execute("""
	update coursestudent set points = 1 where grade = 'C+';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'C';
   	""")
   
   	cur.execute("""
   	update coursestudent set points = 0 where grade = '';
   	""")
   
   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'C-';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'D+';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'D';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'D-';
   	""")

   	cur.execute("""
   	update coursestudent set points = 0 where grade = 'F';
   	""")

   	cur.execute("""
   	update coursestudent set points = 0 where grade = 'NS';
   	""")

   	cur.execute("""
   	update coursestudent set points = 0 where grade = 'NP';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'IP';
   	""")
   	
   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'WD2';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'W04';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'S';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'P';
   	""")

   	cur.execute("""
   	update coursestudent set points = 0 where grade = 'U';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'NG';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'WDC';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'WD1';
   	""")

   	cur.execute("""
   	update coursestudent set points = 1 where grade = 'WN';
   	""")

   	cur.execute("""
   	update coursestudent set points = 0 where grade = 'Y';
   	""")

   	cur.execute("""
   	select distinct coursename from (select coursename,AVG(points) as score from (select * from (select CONCAT(subj,crse) as coursename ,grade,points from coursestudent,courseadministrative where coursestudent.cid = courseadministrative.cid and coursestudent.term = courseadministrative.term)as F) as P group by coursename) as Q where score = 1;
   	""")

   	print("courses with highest pass rate ")

   	result = cur.fetchone()
   	while result is not None:
     		print(str(result[0]))
     		result = cur.fetchone()

   	cur.execute("""
   	select distinct coursename from (select coursename, AVG(points) as score from (select * from (select CONCAT(subj,crse) as coursename ,grade,points from coursestudent,courseadministrative where coursestudent.cid = courseadministrative.cid and coursestudent.term = courseadministrative.term)as F) as P group by coursename) as Q where score = 0.75;
   	""")

   	print("courses with average pass rate lowest")
   	result = cur.fetchone()
   	while result is not None:
     		print(str(result[0]))
     		result = cur.fetchone()

   	cur.execute(""" 
   	alter table coursestudent drop column points;
   	""")
	print("\n")
   
def prob3e():
	print("Executing 3E Code:\n")
	cur.execute("""
	select distinct result.crse AS Answer
	from ((select CIDB AS CID
		from ((select CID AS CIDA, Term, Instructor, Type, Days, Time, Build, Room
			from meeting) AS mA 
			natural join 
			(select CID AS CIDB, Term, Instructor, Type, Days, Time, Build, Room
			from meeting) AS mB) AS combo
		where combo.CIDA > combo.CIDB limit 1000) AS preAns
		natural join
		(select CID, crse
		 from courseadministrative) AS courseadminMod) AS result
	ORDER BY result.crse;
	""")
	result = cur.fetchall()
	print("\nCourses with a cross listed course:")
	for i in range(len(result)):
		print(result[i][0])
	print("\n")
		
def prob3f():
	print("Executing 3F Code:\n")
	cur.execute(""" 
	alter table coursestudent add column points float;
	""")
	cur.execute("""
	update coursestudent set points = 4.0 where grade = 'A+';
	""")

	cur.execute("""
	update coursestudent set points = 4.0 where grade = 'A';
	""")

	cur.execute("""
	update coursestudent set points = 3.7 where grade = 'A-';
	""")

	cur.execute("""
	update coursestudent set points = 3.3 where grade = 'B+';
	""")

	cur.execute("""
	update coursestudent set points = 3.0 where grade = 'B';
	""")

	cur.execute("""
	update coursestudent set points = 2.7 where grade = 'B-';
	""")

	cur.execute("""
	update coursestudent set points = 2.3 where grade = 'C+';
	""")

	cur.execute("""
	update coursestudent set points = 2.0 where grade = 'C';
	""")

	cur.execute("""
	update coursestudent set points = 1.7 where grade = 'C-';
	""")

	cur.execute("""
	update coursestudent set points = 1.3 where grade = 'D+';
	""")

	cur.execute("""
	update coursestudent set points = 1.0 where grade = 'D';
	""")

	cur.execute("""
	update coursestudent set points = 0.7 where grade = 'D-';
	""")

	cur.execute("""
	update coursestudent set points = 0.0 where grade = 'F';
	""")

	cur.execute("""
	update coursestudent set points = 0.0 where grade = 'I';
	""")

	cur.execute("""
	select DISTINCT(major) from (select sid from (select sid,avg(points) as MaxPoint from coursestudent,courseadministrative where subj = 'ABC' and grade!= 'U' and grade!='Y' and grade!='' and grade != 'WN' and grade != 'P' and grade != 'NP' and grade !='S' and grade != 'NS'  and grade != 'WD2' and grade != 'W04' and grade!= 'NG' and grade != 'WDC' and grade != 'WD1' and grade!= 'WN' and grade!='IP' and coursestudent.cid = courseadministrative.cid and coursestudent.term = coursestudent.term group by sid)as DD where MaxPoint in (0,4)) as CV natural join academicinfo where CV.sid = academicinfo.sid;
	""")
	
	result = cur.fetchone()
	#print("Instructor with difficult marking "+str(result))
	while result is not None:
		print(str(result[0]))
		result = cur.fetchone()

	cur.execute(""" 
	alter table coursestudent drop column points;
	""")   
	print("\n")

def prob3g():
	print("Executing 3G Code:\n")
        cur.execute("""
	select sum(WE) from (
	select Q.major,count(Q.sid)  as WE from (select sid,term,major from coursestudent natural join academicinfo)as P, (select sid,term,major from coursestudent natural join academicinfo )as Q where P.sid = Q.sid and Q.term<P.term and Q.major not like 'ABC%' and P.major like 'ABC%' group by Q.major order by count(Q.sid) DESC) as DDF;
 	""")

	result = cur.fetchone()
	k = str(result[0])
	#print(result[0])

	cur.execute("""
	select Q.major,count(Q.sid)/CAST("""+k+"""as float) * 100 as Percentage from (select sid,term,major from coursestudent natural join academicinfo)as P, (select sid,term,major from coursestudent natural join academicinfo )as Q where P.sid = Q.sid and Q.term<P.term and Q.major not like 'ABC%' and P.major like 'ABC%' group by Q.major order by count(Q.sid) DESC LIMIT 5;
	""") 

	result = cur.fetchall()
	print(result)

def prob3h():
	print("Executing 3H Code:\n")
	cur.execute("""
	select sum(WE) from (
	select Q.major,count(Q.sid)  as WE from (select sid,term,major from coursestudent natural join academicinfo)as P, (select sid,term,major from coursestudent natural join academicinfo )as Q where P.sid = Q.sid and Q.term>P.term and Q.major not like 'ABC%' and P.major like 'ABC%' group by Q.major order by count(Q.sid) DESC) as DDF;
 	""")

	result = cur.fetchone()
	k = str(result[0])
	#print(result[0])

        cur.execute("""
	select Q.major,count(Q.sid)/CAST("""+ k +"""as float) * 100 as Percentage from (select sid,term,major from coursestudent natural join academicinfo)as P, (select sid,term,major from coursestudent natural join academicinfo )as Q where P.sid = Q.sid and Q.term>P.term and Q.major not like 'ABC%' and P.major like 'ABC%' group by Q.major order by count(Q.sid) DESC LIMIT 5;
	""") 

	result = cur.fetchall()
	print(result)

def main():
	prob3a()
	prob3b()
  	prob3c()
        prob3d()
	prob3e()
	prob3f()
	prob3g()
        prob3h()   

if __name__ == "__main__":
    main()
