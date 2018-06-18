import os
import psycopg2
import csv
import glob
import sys

conn = psycopg2.connect("dbname=FakeUData")

cur = conn.cursor()

#Problem 3a-------------------------------------------------------------------------------------
cur.execute("""
select count(distinct combo.SID)
from (student natural join CourseAdministrative) AS combo
where combo.Subj = 'ABC' OR combo.Subj = 'DEF';
""")

total = cur.fetchone()

studentUnits = []

for i in range(1, 21):
	cur.execute("""
	select count(studentsTakeUnits.SID) AS answer
	from (select Term, SID, SUM(Units) as totalUnits
		from (coursestudent natural join CourseAdministrative) AS combo
		where combo.Subj = 'ABC' OR combo.Subj = 'DEF'
		GROUP BY Term, SID, Units
		) AS studentsTakeUnits
	where totalUnits = """ + str(i) + """;
	""")
	result = cur.fetchone()
	print(result[0])
	print("Units " + str(i) + ": " + str(result[0] / float(total[0]) * 100))
	studentUnits.append(result[0])


#Problem 3c-----------------------------------------------------------------------------------
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
			from coursestudent
			GROUP BY SID, Term, Units
			) AS studentSTS
		where studentSTS.totalUnitsPerTerm = 1
		) AS studentST
		natural join
	     (select SID, Term, Grade, Points
		from coursestudent natural join gpa
		where Grade IS NOT NULL
		) AS studentSTGP
		) AS result
	GROUP BY Points;
	""")
	print(cur.fetchall())
	#result = cur.fetchone()
	#print("Average GPA of students taking " + str(i) + " units: " + str(result[0]))
	#totalGPA.append(result[0]) 
	#print("Average GPA of students taking " + str(i) + " units: " + str(float(totalGPA[i-1]) / int(totalNumStudentsEachUnit[i - 1])))


