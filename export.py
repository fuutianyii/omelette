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

num=0
now=datetime.datetime.now()
date=""
for i in data:
    i=list(i)
    if num%101==0:
         delta=datetime.timedelta(days=num)
         date=(now+delta).strftime("%Y-%m-%d")
         i[3]=date
         num+=1
    i[3]=date
    print(i)
    sql=f"INSERT INTO words VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', 0,'wrong');"
    cursor.execute(sql)
    con.commit()
    num+=1



print(now.strftime("%Y-%m-%d"))
print((now+delta).strftime("%Y-%m-%d"))
