import sqlite3
import base64
import re

con = sqlite3.connect("db/Oxford.db")
cursor=con.cursor()
for id in range(1,38653):
    sql = f"select rowid,* from words where rowid={id}"
    cursor.execute(sql)
    data=cursor.fetchone()
    dedata=base64.b64decode(data[2]).decode()
    # dedata=dedata.replace(dedata[dedata.find("<font color=red>"):dedata.find("</font>")+7], "").replace("<br>", "",1).replace("green", "grey").replace("blue", 'black')
    # regulation=re.compile("<font color=black>.*?</font><br>")
    # redata=re.findall(regulation, dedata)
    # for exmple in redata:
        #dedata=dedata.replace(exmple, "<ul><li>"+exmple.replace("<br>", "")+"</li></ul>").replace("&nbsp;&nbsp;&nbsp;&nbsp;", "").replace("color=\"#F17D1F\"", "color=\"\"")
    # dedata=dedata.replace("red", "''")
    dedata=dedata.replace("size=4", "''")
    endata=base64.b64encode(dedata.encode()).decode()
    sql=f"update words set sentence='{endata}' where rowid={id}"
    cursor.execute(sql)
    con.commit()
    print(id)


