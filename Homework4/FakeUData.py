import os
import psycopg2
import csv
import glob
import sys

conn = psycopg2.connect("dbname=FakeUData")

cur = conn.cursor()

cur.execute("CREATE TABLE Student(SID varchar(50),Surname varchar(20),Prefname varchar(20),Email varchar(50))")

cur.execute("CREATE TABLE AcademicInfo(Level varchar(10),Email varchar(50),Major varchar(50),SID integer,Class varchar(40))")

cur.execute("CREATE TABLE CourseStudent(Seat integer,Grade varchar(30),Status varchar(30),SID integer,CID varchar(5),Email varchar(50),Term INTEGER,Units float)")

cur.execute("CREATE TABLE Course(CID VARCHAR(5),TERM INTEGER,SEC VARCHAR(20),PRIMARY KEY(CID,TERM))")

cur.execute("CREATE TABLE CourseAdministrative(MinUnits float,MaxUnits float,Subj varchar(50),Crse varchar(50),CID VARCHAR(5),TERM INTEGER,PRIMARY KEY(CID,TERM))")
 
cur.execute("CREATE TABLE Meeting(CID VARCHAR(5), TERM INTEGER, INSTRUCTOR varchar(100),TYPE varchar(150),Days varchar(120),time varchar(100), BUILD VARCHAR(100),ROOM varchar(50))")
#######################################################################################
############################Inserting into course db###################################
#######################################################################################

#change directory depending on whether an argument was passed in
if (len(sys.argv) == 1):
	os.chdir(".")
else:
	os.chdir(sys.argv[1])

#use sets instead of arrays, much fast
#hash table vs n searches
sidlist = set([])
emaillist= set([])
cidlist2= set([])
prevInst = ""
flagg = 1
#iterate through all csv files and perform operations
for i in glob.glob("*.csv"):
   Test = csv.reader(open(i))
   print(i)
   next(Test)
   next(Test)
   statement = "INSERT INTO Course VALUES"
   statement1 = "INSERT INTO CourseAdministrative VALUES"
   count = 0
   flag = 0
   linecount=1
   cidtermlist=[]
   for tuple in Test:
   #print(tuple[0]);
   #print(tuple)
      linecount=linecount+1;
      minunits = 0.00
      maxunits = 0.00
      if(flag == 1):
        flag = 0
        continue
      if not ''.join(tuple).strip():
         if (count == 2):
             count = 0
             f = 2
             if("INSERT INTO Student VALUES" == statement2):
               f=0
             g = 2
             if("INSERT INTO AcademicInfo VALUES" == statement3):
               g=0
             k = 2
             if("INSERT INTO CourseStudent VALUES" == s4):
               k=0
             statement2 = statement2[:-1]
             statement2 += ";"
             s4 = s4[:-1]
             s4 += ";"
          #print(statement2)
             statement3 = statement3[:-1]
             statement3 += ";"
             if (f == 2):
               cur.execute(statement2);
             if(g == 2):
               cur.execute(statement3);
             if(k == 2):
               cur.execute(s4);
          #statement1 = statement1[:-1]
          #statement1 += ";"
          #cur.execute(statement1);
             statement = "INSERT INTO Course VALUES"
             statement1 = "INSERT INTO CourseAdministrative VALUES"
             flag=1
             continue
         elif (count == 0):
             count = count + 1
             flag=1
             statement = statement[:-1]
             statement += ";"
             wx=2
             if("INSERT INTO Course VALUE;" == statement):
               wx=0
             if(wx == 2):
               cur.execute(statement)
             statement1 = statement1[:-1]
             statement1 += ";"
             pr = 2
             if("INSERT INTO CourseAdministrative VALUE;" == statement1):
               pr=0
             if(pr == 2):
               cur.execute(statement1)
             statement = "INSERT INTO Meeting VALUES"         
             continue
         elif (count == 1):
             count = count + 1
             flag=1
             qq=2
             if(statement == "INSERT INTO Meeting VALUES"):
               qq=0
             #cur.execute(statement)
             statement = statement[:-1]
             statement += ";"
             if(qq==2):
              cur.execute(statement)
          #print(count)
             statement2 = "INSERT INTO Student VALUES"         
             statement3 = "INSERT INTO AcademicInfo VALUES"
             s4 = "INSERT INTO CourseStudent VALUES"
             continue

   
      if(count == 0):
        if(not((tuple[0],tuple[1]) in cidlist2)):
          statement += "('%s', %d, '%s'),"%(tuple[0],int(tuple[1]),tuple[4])
        minunits = 0.00   
        maxunits = 0.00
        if(" - " in tuple[5]):
           r = tuple[5].split(" - ");
           minunits = float(r[0])
           maxunits = float(r[1])
        #print(r[0])
        #print(r[1])
        else:
        #print(tuple[5])
        #print(linecount)
           minunits = float(tuple[5])
           maxunits = float(tuple[5])
        if(not((tuple[0],tuple[1]) in cidlist2)):
         statement1 +="(%f,%f,'%s','%s','%s',%d),"%(minunits,maxunits,tuple[2],tuple[3],tuple[0],int(tuple[1]))
        cidtermlist.append((tuple[0],tuple[1]))
        cidlist2.add((tuple[0],tuple[1]))

      if(count == 1):
        cidtermset = set(cidtermlist)
        cidtermlist = list(cidtermset)
        f=tuple[0]
        if("'" in tuple[0]):
	   f = f.replace("'", "")
        if(prevInst == "" and flagg == 1 and tuple[0] != ""):
             f = tuple[0]
             prevInst = tuple[0]
        elif(prevInst != "" and flagg == 0):
           if(tuple[0] == ""):
             f = prevInst
           else:
             f = tuple[0]
             prevInst = tuple[0]
        if("'" in f):
           f = f.replace("'", "")
        flagg = 0

        #print(tuple[2],tuple[3],tuple[4],tuple[5])
        #print(type(tuple[2]),type(tuple[3]),type(tuple[4]),type(tuple[5]))
        for i in range(len(cidtermlist)):
           r = cidtermlist[i][0]
           x = cidtermlist[i][1]
           statement += "('%s',%d,'%s','%s','%s','%s','%s','%s'),"%(r,int(x),f,tuple[1],tuple[2],tuple[3],tuple[4],tuple[5])
     #cidlist = []
#cur.execute(statement);
########################################################################################
########################################################################################
      if(count == 2):
     #print("hi")
        o = tuple[2]
        if("'" in o):
	   o = o.replace("'", "")
        z = tuple[10]
        if("'" in tuple[10]):
           z = z.replace("'", "")

	sidlist.add(int(tuple[1]))
	emaillist.add(z)
        statement2 += "('%s','%s','%s','%s')," %(tuple[1],o,tuple[3],z)
        statement3 += "('%s','%s','%s','%s','%s')," %(tuple[4],z,tuple[7],tuple[1],tuple[6])
     #print(s4)
       
        for i in range(len(cidtermlist)):
           r = cidtermlist[i][0]
           y = cidtermlist[i][1]
           s4 += "(%d,'%s','%s','%s','%s','%s',%d,%f)," %(int(tuple[0]),tuple[8],tuple[9],tuple[1],r,z,int(y),float(tuple[5]))
        cidtermlist = []
        flagg=1

conn.commit()
