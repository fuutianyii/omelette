import sqlite3
import datetime


con = sqlite3.connect("words.db")
cursor=con.cursor()
sql="select * from words  where wrong_times != '0';"
data=cursor.execute(sql)
con.commit()

con = sqlite3.connect("forgot.db")
cursor=con.cursor()
sql =sql = "CREATE TABLE IF NOT EXISTS words(english text not null,chinese text not null,posd text not null,insert_date text not null,wrong_times INTEGER not null,list text)"
cursor.execute(sql)
con.commit()
inum=0
num=0
now=datetime.datetime.now()
date=""
for i in data:
    i=list(i)
    if inum%100==0:
         delta=datetime.timedelta(days=num)
         date=(now+delta).strftime("%Y-%m-%d")
         i[3]=date
         num+=1
         print("-------------------")
    i[3]=date
    i[4]=0
    sql=f"INSERT INTO words VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}','wrong');"
    cursor.execute(sql)
    con.commit()
    inum+=1
