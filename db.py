#!python3.8
#-*- coding: utf-8 -*-
'''
Author: fuutianyii
Date: 2022-09-10 15:40:07
LastEditors: fuutianyii
LastEditTime: 2022-09-18 10:46:31
github: https://github.com/fuutianyii
mail: fuutianyii@gmail.com
QQ: 1587873181
'''
import sqlite3

class db():
    def __init__(self,dbname="db/words.db"):
        self.con = sqlite3.connect(dbname)
        self.cursor=self.con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS words(english text not null,chinese text not null,posd text not null,insert_date text not null,wrong_times INTEGER not null)"
        self.cursor.execute(sql)

    def insert(self,english,chinese,posd,insert_date,wrong_times,list):
        chinese=chinese.replace("'","''") #sqllite转义单引号 ’=>''
        sql=f"INSERT INTO words VALUES ('{english}', '{chinese}', '{posd}', '{insert_date}', {wrong_times},'{list}');"
        self.cursor.execute(sql)
        self.con.commit()

    def select(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self,sql):
        self.cursor.execute(sql)
        self.con.commit()

    def delete(self,sql):
        self.cursor.execute(sql)
        self.con.commit()


if  __name__ =="__main__":
    db=db()
    # db.insert('brand', '品牌', 'n', '今天是：2022年04月22日', 0)
    print(db.select("SELECT rowid,* FROM words where english='brand'"))