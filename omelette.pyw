# !/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: fuutianyii
Date: 2022-08-21 09:29:29
LastEditors: fuutianyii
LastEditTime: 2022-08-23 21:29:00
github: https://github.com/fuutianyii
mail: fuutianyii@gmail.com
QQ: 1587873181
'''
import Ui_UI
import db
import youdao
import sys
import datetime
from time import sleep
from os import getcwd,path
from requests import get
from time import localtime,strftime
from random import randrange,shuffle
from base64 import b64decode
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QItemDelegate,QMessageBox,QAbstractItemView,QHeaderView,QSizePolicy
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer 
from PyQt5.QtCore import Qt,QUrl 
from PyQt5.QtGui import QPixmap,QIcon

class EmptyDelegate(QItemDelegate):
    def __init__(self,parent):
        super(EmptyDelegate, self).__init__(parent)
    
    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None

# https://dict.youdao.com/example/blng/eng/tutor/#keyfrom=dict.main.moreblng

class mainwindow(Ui_UI.Ui_MainWindow,QMainWindow):  
    def __init__(self):
        super().__init__()
        self.youdao=youdao.youdao_api()
        self.mydb=db.db("db/words.db")
        # self.mydb=db.db("db/forgot.db")
        self.myOxford=db.db("db/Oxford.db")
        self.get_all_list()
        self.get_all_insert_date()
        self.player = QMediaPlayer() 
        self.datetime=strftime("%Y-%m-%d",localtime())
        self.setupUi(self)
        self.remake_ui()
        self.condef()
        self.autostart()    
        self.lens=1
        self.group=""
        self.date="全部时间"
        self.list="全部分组"
        self.forgeted=0
        
    def  clear_add_chinese_table(self):
        for i in range(1,self.lens+1):
            self.add_chinese_input_table_widget.removeRow(0)
            self.lens=1

    def autostart(self):
        self.Stacked.setCurrentIndex(0)

    def remake_ui(self):
        self.seach_input_edit.setPlaceholderText("搜索单词")
        self.seach_input_edit.setStyleSheet("border:0px;background:rgba(255,255,255,1);border-radius: 15px;margin:10px;padding:0px 20px")
        self.leftframe.setStyleSheet("background:rgba(240,240,240,1);")
        self.homepage_left.setStyleSheet("background:rgba(240,240,240,1);")
        #居中
        self.forget_label.setAlignment(Qt.AlignCenter)
        # self.hello_text.setAlignment(Qt.AlignCenter)
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/homepage.png"), QIcon.Normal, QIcon.Off)
        self.left_first_button.setIcon(icon)
        self.left_first_button.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/search.png"), QIcon.Normal, QIcon.Off)
        self.left_second_button.setIcon(icon)
        self.left_second_button.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star_book.png"), QIcon.Normal, QIcon.Off)
        self.left_third_button.setIcon(icon)
        self.left_third_button.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting.png"), QIcon.Normal, QIcon.Off)
        self.left_forth_button.setIcon(icon)
        self.left_forth_button.setStyleSheet("background:rgba(0,0,0,0);")

        #更改字符
        time_str=strftime("%Y %m %d",localtime())
        time_list=time_str.split(" ")
        
        month_list=["January","February","March","April","May","June","July","August","September","October","November","December"]
        month=month_list[int(time_list[1])-1]
        if time_list[2]=="01":
            time_list[2]="1st"
        elif time_list[2]=="02":
            time_list[2]="2nd"
        elif time_list[2]=="03":
            time_list[2]="3rd"
        else:
            time_list[2]=str(int(time_list[2]))+"th"
        self.hello_text.setText(month +" "+time_list[2])
        #num=0 #这里获取录入了多少个单词
        self.all_words_num=self.mydb.select("SELECT Count(*) FROM words")[0][0]
        self.online_youdao_textBoswer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.online_youdao_textBoswer.setStyleSheet("QTextBrowser{border:none;font-size:15px;background:rgba(0,0,0,0);}")
        self.youdao_textBrowswer.setStyleSheet("QTextBrowser{border:none;font-size:15px;background:rgba(0,0,0,0);}")
        
        self.youdao_textBrowswer.setTextInteractionFlags(Qt.NoTextInteraction)
        self.Oxford_info_box.setStyleSheet("QTextBrowser{border:none;font-size:15px;background:rgba(0,0,0,0);}")
        
        self.Oxford_info_box.setTextInteractionFlags(Qt.NoTextInteraction)
        self.Oxford_info_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.english_input_edit.setStyleSheet("border: none;border-radius: 15px;font-size:40px;padding-left:20px;background:rgba(240,240,240,1)")
        self.update_table.setStyleSheet("""QTableWidget{border:none;selection-background-color:white;selection-color:black;}QScrollBar:vertical{ width:8px;border-style:flat;border-radius: 4px;border:0px;background: rgba(0,0,0,0);} QScrollBar::handle:vertical{ background: rgba(0,0,0,0.20);border-radius: 4px;width:8px; min-height:91px; border-style:flat;}QScrollBar::handle:vertical::hover{ background: rgba(0,0,0,0.40);border-radius: 4px;width:8px; }QScrollBar::handle:vertical::pressed{ background: rgba(0,0,0,0.40);border-radius:4px;width:8px; }QScrollBar::sub-page:horizontal {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::add-page:horizontal {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::sub-line:horizontal {background: rgba(0,0,0,0);}QScrollBar::add-line:horizontal{background: rgba(0,0,0,0);}QScrollBar::sub-page:vertical {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::add-page:vertical {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::add-line:vertical{background: rgba(0,0,0,0);}QScrollBar::sub-line:vertical {background: rgba(0,0,0,0);}QScrollBar:horizontal{ height:8px;border-style:flat;border-radius: 4px;border:0px;background: rgba(0,0,0,0);} QScrollBar::handle:horizontal{ background: rgba(0,0,0,0.20);border-radius: 4px;height:8px; min-width:91px; border-style:flat;}QScrollBar::handle:horizontal::hover{ background: rgba(0,0,0,0.40);border-radius: 4px;height:8px; }QScrollBar::handle:horizontal::pressed{ background: rgba(0,0,0,0.40);border-radius:4px;height:8px; }QScrollBar::sub-page:horizontal {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::add-page:horizontal {background: rgba(0,0,0,0);border-style:flat;}QScrollBar::sub-line:horizontal {background: rgba(0,0,0,0);}QScrollBar::add-line:horizontal{background: rgba(0,0,0,0);}""")
        self.update_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table.setFocusPolicy(Qt.NoFocus)
        #取消虚线框
        self.update_table.setShowGrid(False)
        #取消网格线
        self.update_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #不可写
        self.update_table.horizontalHeader().setVisible(False)
        # self.update_table.verticalHeader().setVisible(False)
        self.update_table.setColumnCount(1)
        self.update_table.setRowCount(self.update_table.rowCount()+1)
        self.update_table.setColumnWidth(0,130)
        self.filter_list_comboBox.addItem("全部分组")
        for list_one in self.all_lists:
            self.filter_list_comboBox.addItem(list_one[0])
        self.filter_list_comboBox.setStyleSheet("""
            QComboBox{
                background: rgba(0,0,0,0);
                border:none;
            }
            QComboBox::down-arrow {
                image: url(:/res/work/dateDown.png);
            }
            """)
        
        self.filter_date_comboBox.addItem("全部时间")
        for date in self.all_insert_dates:
            self.filter_date_comboBox.addItem(date[0])
        self.filter_date_comboBox.setStyleSheet("""
            QComboBox{
                background: rgba(0,0,0,0);
                border:none;
            }
            QComboBox::down-arrow {
                image: url(:/res/work/dateDown.png);
            }
            """)
        self.search_edit.setStyleSheet("border: none;border-radius: 10px;font-size:15px;background:rgba(240,240,240,1)")
        self.search_edit.setPlaceholderText("搜索单词")
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting.png"), QIcon.Normal, QIcon.Off)
        self.more_functions.setIcon(icon)
        self.more_functions.setStyleSheet("background:rgba(0,0,0,0);")
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/sync.png"), QIcon.Normal, QIcon.Off)
        self.Sync.setIcon(icon)
        self.Sync.setStyleSheet("background:rgba(0,0,0,0);")
    
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/sync.png"), QIcon.Normal, QIcon.Off)
        self.Sync.setIcon(icon)
        self.Sync.setStyleSheet("background:rgba(0,0,0,0);")
      
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/search.png"), QIcon.Normal, QIcon.Off)
        self.display_search_line_edit.setIcon(icon)
        self.display_search_line_edit.setStyleSheet("background:rgba(0,0,0,0);")
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/start.png"), QIcon.Normal, QIcon.Off)
        self.start_exam.setIcon(icon)
        self.start_exam.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/forget.png"), QIcon.Normal, QIcon.Off)
        self.search_forget_words.setIcon(icon)
        self.search_forget_words.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star.png"), QIcon.Normal, QIcon.Off)
        self.star.setIcon(icon)
        self.star.setStyleSheet("background:rgba(0,0,0,0);")

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/voice.png"), QIcon.Normal, QIcon.Off)
        self.play_voice_1.setIcon(icon)
        self.play_voice_1.setStyleSheet('text-align:center;background:rgba(235,235,235,0.9);border:none;border-radius:10px;vertical-align: middle;')
        self.play_voice_1.adjustSize()
        self.play_voice_2.setIcon(icon)
        self.play_voice_2.setStyleSheet('text-align:center;background:rgba(235,235,235,0.9);border:none;border-radius:10px;vertical-align: middle;')
        self.play_voice_2.adjustSize()
        self.online_play_voice_1.setIcon(icon)
        self.online_play_voice_1.setStyleSheet('text-align:left;background:rgba(255,255,255,0.8);border:none;border-radius:10px;')
        self.online_play_voice_1.adjustSize()
        self.online_play_voice_2.setIcon(icon)
        self.online_play_voice_2.setStyleSheet('text-align:left;background:rgba(255,255,255,0.8);border:none;border-radius:10px;')
        self.online_play_voice_2.adjustSize()
        self.word_info_table.setColumnCount(2)
        self.word_info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.word_info_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.word_info_table.setColumnWidth(0, 50)
        self.word_info_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.word_info_table.setFocusPolicy(Qt.NoFocus)
        #取消虚线框
        self.word_info_table.setShowGrid(False)
        #取消网格线
        self.word_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #不可写
        self.word_info_table.horizontalHeader().setVisible(False)
        self.word_info_table.verticalHeader().setVisible(False)
        self.word_info_table.setStyleSheet("QTableWidget{border:none;font-size:15px}QTableWidget::item::selected {background:rgb(255,255,255);}")
        self.word_info_table.setWordWrap(True)
        # self.word_info_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.word_info_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabWidget.setStyleSheet("QTabWidget{border:none;}QTabWidget::pane{border:none;}QTabWidget::tab-bar {left: 5px;}QTabBar::tab { border-bottom-color: #C2C7CB;border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 60px;padding: 2px;}QTabBar::tab:selected{background:rgb(255,255,255);}QTabBar::tab:selected{background:rgb(245,245,245);}QTabBar::tab:!selected{margin-top:5px;}/*四个下属界面*/#tab,#tab_2,#tab_3,#tab_4{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454)border-radius:6px;}")
        self.online_Oxford_info_box.setStyleSheet("QTextBrowser{border:none;font-size:15px;background:rgba(0,0,0,0);}")
        self.online.setStyleSheet("QTabWidget{border:none;}QTabWidget::pane{border:none;}QTabWidget::tab-bar {left: 5px;}QTabBar::tab { border-bottom-color: #C2C7CB;border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 60px;padding: 2px;}QTabBar::tab:selected{background:rgb(255,255,255);}QTabBar::tab:selected{background:rgb(245,245,245);}QTabBar::tab:!selected{margin-top:5px;}/*四个下属界面*/#tab,#tab_2,#tab_3,#tab_4{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454)border-radius:6px;}")
        QApplication.processEvents()


    def condef(self):
        self.english_input_edit.returnPressed.connect(self.display_online)
        self.seach_input_edit.returnPressed.connect(self.homepage_to_search)
        self.left_first_button.clicked.connect(self.changepage_main)
        self.left_second_button.clicked.connect(self.changepage_add)
        self.left_third_button.clicked.connect(self.changepage_update)
        self.left_forth_button.clicked.connect(self.changepage_exam)
        # self.add_english_input_next.clicked.connect(self.change_add_frame_to_part_of_speech)
        # self.add_english_input_edit.returnPressed.connect(self.change_add_frame_to_part_of_speech)
        # self.add_part_of_speech_input_next.clicked.connect(self.change_add_frame_to_chinese)
        # self.add_part_of_speech_input_last.clicked.connect(self.back_add_english_widget)
        # self.add_chinese_input_last.clicked.connect(self.back_add_frame_to_part_of_speech)
        # self.add_chinese_input_next.clicked.connect(self.complete_one)
        self.search_edit.returnPressed.connect(self.update_page_search)
        self.star.clicked.connect(self.star_the_word)
        self.exam_calendarWidget.clicked.connect(self.start_choose_exam)
        # self.update.clicked.connect(self.update_all_words)
        self.forget_pushButton.clicked.connect(self.display_forget)
        # self.delete_choose.clicked.connect(self.delete_words)
        self.exam_english_lable.returnPressed.connect(self.exam_submit)
        self.change_calendar.clicked.connect(self.changepage_exam_calendar)
        self.back_exam_main.clicked.connect(self.changepage_exam_main)
        self.exam_today_button.clicked.connect(self.today_exam)
        self.review_words_button.clicked.connect(self.review_words)
        self.radom_exam_button.clicked.connect(self.random_exam)
        self.review_Forgotten_button.clicked.connect(self.forgoten_exam)
        self.remove_forget_pushButton.clicked.connect(self.reset_wrong_times)
        self.update_table.itemClicked.connect(self.show_defined_selection)
        self.play_voice_1.clicked.connect(self.play_the_word_uk)
        self.play_voice_2.clicked.connect(self.play_the_word_us)
        self.start_exam.clicked.connect(self.exam_choose_words)
        
        # self.filter_list_comboBox.currentIndexChanged.connect(self.update_page_search)
        # self.filter_date_comboBox.currentIndexChanged.connect(self.update_page_search)
        self.filter_list_comboBox.currentIndexChanged.connect(self.filter_list)
        self.filter_date_comboBox.currentIndexChanged.connect(self.filter_date)
        self.search_forget_words.clicked.connect(self.select_forget_words)


    def star_the_word(self):
        if self.list_line.text().replace(" ", "") == "":
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '请输入list')
            msg_box.exec_()
        else:
            search=f"select english from words where english='{self.english_input_edit.text()}'"
            if len(self.mydb.select(search)) ==  0:
                self.online_dict[0][0]
                for word in self.online_dict:
                    self.mydb.insert(word[0],word[4],word[3],self.datetime,0,self.list_line.text().replace(" ", ""))
                icon = QIcon()
                icon.addPixmap(QPixmap("ico/un_star.png"), QIcon.Normal, QIcon.Off)
                self.star.setIcon(icon)
                self.star.setStyleSheet("background:rgba(0,0,0,0);")
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '添加成功')
                msg_box.exec_()
            else:
                icon = QIcon()
                icon.addPixmap(QPixmap("ico/star.png"), QIcon.Normal, QIcon.Off)
                self.star.setIcon(icon)
                self.star.setStyleSheet("background:rgba(0,0,0,0);")
                delete=f"delete from words where english='{self.english_input_edit.text()}'"
                self.mydb.delete(delete)
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '删除成功')
                msg_box.exec_()

        
    def homepage_to_search(self):
        self.Stacked.setCurrentIndex(1)
        self.english_input_edit.setText(self.seach_input_edit.text())
        self.online_dict=self.youdao.main_no_print_online(self.seach_input_edit.text()) 
        self.online_play_voice_1.setText(self.online_dict[0][1]+"  ")
        self.online_play_voice_2.setText(self.online_dict[0][2]+"  ")
        display_data="<table><tr>"
        for data in self.online_dict:
            display_data+="<td>"+data[3]+"</td><td> "+data[4]+"</td></tr><tr>"
        display_data+="</table>"+data[5].replace("\n","<br>")
        display_data+="<h2>例句</h2>"+data[6]
        self.online_youdao_textBoswer.setText(display_data)
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+self.english_input_edit.text()+"'")
            b64decode(Oxford_data[0][1]).decode()
            self.online_Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.online_Oxford_info_box.setText("暂无数据")
        search=f"select english from words where english='{self.english_input_edit.text()}'"
        if len(self.mydb.select(search)) ==  0:
            icon = QIcon()
            icon.addPixmap(QPixmap("ico/star.png"), QIcon.Normal, QIcon.Off)
            self.star.setIcon(icon)
            self.star.setStyleSheet("background:rgba(0,0,0,0);")
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap("ico/un_star.png"), QIcon.Normal, QIcon.Off)
            self.star.setIcon(icon)
            self.star.setStyleSheet("background:rgba(0,0,0,0);")
        QApplication.processEvents()


    def display_online(self):
        self.online_dict=self.youdao.main_no_print_online(self.english_input_edit.text()) 
        self.online_play_voice_1.setText(self.online_dict[0][1]+"  ")
        self.online_play_voice_2.setText(self.online_dict[0][2]+"  ")
        display_data="<table><tr>"
        for data in self.online_dict:
            display_data+="<td>"+data[3]+"</td><td> "+data[4]+"</td></tr><tr>"
        display_data+="</table>"+data[5].replace("\n","<br>")
        display_data+="<h2>例句</h2>"+data[6]
        self.online_youdao_textBoswer.setText(display_data)
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+self.english_input_edit.text()+"'")
            b64decode(Oxford_data[0][1]).decode()
            self.online_Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.online_Oxford_info_box.setText("暂无数据")
        search=f"select english from words where english='{self.english_input_edit.text()}'"
        if len(self.mydb.select(search)) ==  0:
            icon = QIcon()
            icon.addPixmap(QPixmap("ico/star.png"), QIcon.Normal, QIcon.Off)
            self.star.setIcon(icon)
            self.star.setStyleSheet("background:rgba(0,0,0,0);")
        else:
            icon = QIcon()
            icon.addPixmap(QPixmap("ico/un_star.png"), QIcon.Normal, QIcon.Off)
            self.star.setIcon(icon)
            self.star.setStyleSheet("background:rgba(0,0,0,0);")
        QApplication.processEvents()
            


    def get_all_insert_date(self):
        search="select insert_date From words Group By insert_date;"
        self.all_insert_dates=self.mydb.select(search)

    def get_all_list(self):
        search="select list From words Group By list;"
        self.all_lists=self.mydb.select(search)

    def play_the_word_uk(self):
        self.play(self.selection_word.text(),1)
    
    def play_the_word_us(self):
        self.play(self.selection_word.text(),2)

    def show_defined_selection(self,Item):
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+Item.text()+"'")
            b64decode(Oxford_data[0][1]).decode()
            self.Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.Oxford_info_box.setText("暂无数据")
        define_word=self.youdao.main_no_print(Item.text(),f"select * from words where (english='{Item.text()}')")
        # print(phonetic_symbol[0][0])
        self.play_voice_label_1.setText("英 /"+define_word[0][1]+"/")
        self.play_voice_label_2.setText("美 /"+define_word[0][2]+"/")

        self.selection_word.setText(Item.text())
        self.insert_date.setText("添加日期："+self.update_words[self.update_table.currentRow()][4])
        self.words_list.setText("组别名称："+self.update_words[self.update_table.currentRow()][6])

        self.word_info_table.setRowCount(1)
        newItem = QTableWidgetItem(self.update_words[self.update_table.currentRow()][3])
        newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.word_info_table.setItem(0,0,newItem)
        
        newItem = QTableWidgetItem(self.update_words[self.update_table.currentRow()][2])
        self.word_info_table.setItem(0,1,newItem)
        
        self.word_info_table.resizeRowsToContents()#自动调整行高度
        self.word_info_table.resizeColumnsToContents()#自动调整列宽

        display_data="<table><tr>"
        for data in define_word:
            display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
        display_data+="</table>"+data[5].replace("\n","<br>")
        display_data+="<h3>例句</h3>"+b64decode(data[6]).decode()

        self.youdao_textBrowswer.setText(display_data)


    def update_all_words(self):
        for i in range(0,self.update_table.rowCount()):
            english=self.update_table.item(i, 0).text()
            chinese=self.update_table.item(i, 1).text()
            posd=self.update_table.item(i, 2).text()
            insert_date=self.update_table.item(i,3).text()
            group=self.update_table.item(i,4).text()
            rowid=self.update_words[i][0]
            self.mydb.update(f"update words set english='{english}',chinese='{chinese}',insert_date='{insert_date}',list='{group}',posd='{posd}' where rowid={rowid}")
        msg_box = QMessageBox(QMessageBox.Warning, '提示','更改成功')
        msg_box.exec_()

    def delete_words(self):
        tablelen=len(self.update_table.selectedIndexes())
        rows=len(self.update_table.selectedIndexes())//4
        if tablelen == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有选中单词')
            msg_box.exec_()
            return 0
        #self.update_table.selectedIndexes() #会一格一格遍历，每一格就是一个列表项
        for index in range(0,tablelen)[::5]:#设置步长为4
            row_index=self.update_table.selectedIndexes()[index+1].row() #获取行号
            row_id=self.update_words[row_index][0]
            sql=f"delete from words where rowid={row_id}"
            self.mydb.delete(sql)
        self.changepage_update()#刷新一波
        msg_box = QMessageBox(QMessageBox.Warning, '警告', f'成功删除{rows}个单词')
        msg_box.exec_()
            
    def exam_choose_words(self):
        if len(self.update_words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到单词')
            msg_box.exec_()
        else:
            self.changepage_exam()
            self.words=self.update_words
            if self.checkBox_random.isChecked():
                self.words=self.words[::-1]
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0):
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)

    def select_forget_words(self):
        for i in range(0,self.update_table.rowCount()+1):
            self.update_table.removeRow(0)
            self.lens=1
        group=""
        search_filter=[]
        if self.date=="全部时间":
            search_filter.append(f" (insert_date != '') ")
        else:
            search_filter.append(f"(insert_date='{self.date}')")
       
        if self.list == "全部分组":
            search_filter.append(f" (list !='')")
        else:
            search_filter.append(f"(list='{self.list}')")

        search="select rowid,* from words where "
        if (len(search_filter) != 0):
            search+=search_filter[0]
            for i in range(1,len(search_filter)):
                search+=" and "
                search+=search_filter[i]
        else:
            search+=" 1=1"
        search += " and (wrong_times != 0) order by 6 desc"
        self.update_words=self.mydb.select(search)
        for items in self.update_words:
            setline=self.update_table.rowCount()+1
            self.update_table.setRowCount(self.update_table.rowCount()+1)
            newItem = QTableWidgetItem(items[1])
            self.update_table.setItem(self.update_table.rowCount()-1,0,newItem)

    def filter_date(self,index):
        date=self.all_insert_dates[index-1][0]
        if index==0:
            search=f"select rowid,* from words where insert_date!=''"
            self.date="全部时间"
        else:
            self.date=date
            if self.list=="全部分组":
                search=f"select rowid,* from words where insert_date='{date}'"
            else:
                search=f"select rowid,* from words where insert_date='{date}' and  list='{self. list}"

        self.update_words=self.mydb.select(search)
        self.update_table.setRowCount(len(self.update_words))
        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)

    def filter_list(self,index):
        list_one=self.all_lists[index-1][0]
        if index==0:
            search=f"select rowid,* from words where list!=''"
            self.list="全部分组"
        else:
            self.list=list_one
            if self.date=="全部时间":
                search=f"select rowid,* from words where list='{list_one}'"
            else:
                search=f"select rowid,* from words where list='{list_one}' and  insert_date='{self.date}'"
        self.update_words=self.mydb.select(search)
        self.update_table.setRowCount(len(self.update_words))
        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)

    def update_page_search(self):
        search="select rowid,* from words where "
        for i in range(0,self.update_table.rowCount()+1):
            self.update_table.removeRow(0)
            self.lens=1
        group=""
        search_filter=[]
        if self.date=="全部时间":
            search_filter.append(f" (insert_date != '') ")
        else:
            search_filter.append(f"(insert_date='{self.date}')")
       
        if self.list == "全部分组":
            search_filter.append(f" (list !='')")
        else:
            search_filter.append(f"(list='{self.list}')")
        
        if (len(search_filter) != 0):
            search+=search_filter[0]
            for i in range(1,len(search_filter)):
                search+=" and "
                search+=search_filter[i]
        else:
            search+=" 1=1"
        
        search += " and ((english like '%"+self.search_edit.text()+"%' ) or (chinese like '%"+self.search_edit.text()+"%' ))"
        self.update_words=self.mydb.select(search)
        self.update_table.setRowCount(len(self.update_words))
        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)
        return self.update_words

    def play(self,word,type):
        try:
            if path.exists(f"mp3/voice_{word}_{type}.mp3") == True:
                # mp3_path=getcwd().replace("\\", "/")+f"\\mp3\\voice_{word}.mp3".replace("\\", "/")
                mp3_path=getcwd().replace("\\", "/")+f"\\mp3\\voice_{word}_{type}.mp3".replace("\\", "/")
                url = QUrl.fromLocalFile(mp3_path)
                content = QMediaContent(url)  # 加载音乐
                self.player.setMedia(content)     # 关联 QMediaPlayer控件与音乐地址
                self.player.play()                          # 播放
            else:
                self.getmp3(word)
                mp3_path=getcwd().replace("\\", "/")+f"\\mp3\\voice_{word}_{type}.mp3".replace("\\", "/")
                url = QUrl.fromLocalFile(mp3_path)
                content = QMediaContent(url)  # 加载音乐
                self.player.setMedia(content)     # 关联 QMediaPlayer控件与音乐地址
                self.player.play()                          # 播放
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '播放失败')
            msg_box.exec_()

    def getmp3(self,word):
        try:
            # respond=get(f"https://fanyi.baidu.com/gettts?lan=en&text={word}&spd=3&source=web")
            respond=get(f"https://dict.youdao.com/dictvoice?audio={word}&type=1")
            if respond.status_code == 200:
                data=respond.content
                w = open(f"mp3/voice_{word}_1.mp3","wb") 
                w.write(data)
                w.close()
                
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '下载音频文件失败，请检查你的网络环境')
                msg_box.exec_()

            respond=get(f"https://dict.youdao.com/dictvoice?audio={word}&type=2")
            if respond.status_code == 200:
                data=respond.content
                w = open(f"mp3/voice_{word}_2.mp3","wb") 
                w.write(data)
                w.close()
                # self.play(word)
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '下载音频文件失败，请检查你的网络环境')
                msg_box.exec_()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '下载失败')
            msg_box.exec_()

    def exam_submit(self):
        if  self.exam_english_lable.text() == self.words[self.words_index][1]:
            self.exam_english_lable.setStyleSheet('''QWidget{background-color:#66FFCC;}''')
            QApplication.processEvents()#刷新样式
            self.exam_english_lable.setText("")
            english=self.words[self.words_index][1]
            if self.checkBox_voice.isChecked():
                self.play(english,1)
                sleep(1)
            self.exam_change()
        else:
            self.exam_english_lable.setStyleSheet('''QWidget{background-color:#FFB6C1;}''')
            self.exam_english_lable.setText("")
    
    def display_forget(self):
        if self.forgeted == 0:
            english=self.words[self.words_index][1]
            wrong_times=self.mydb.select(f"select wrong_times from words where english='{english}'")[0][0]
            wrong_times=self.mydb.update(f"update words set wrong_times={wrong_times+1} where english='{english}'")
            self.forget_label.setText(self.words[self.words_index][1])
        self.forgeted=1

    def reset_wrong_times(self):
        english=self.words[self.words_index][1]
        wrong_times=self.mydb.update(f"update words set wrong_times=0 where english='{english}'")

    def exam_change(self):
        self.forgeted = 0
        self.words_index+=1
        if  len(self.words) == self.words_index:
           self.exam_stacked.setCurrentIndex(0)
           self.words_index=0
        else:
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            if (self.words[self.words_index][5] !=0):
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)
                
    def start_choose_exam(self):
        date=str(self.exam_calendarWidget.selectedDate().toPyDate())#获取选中日期并且转为str格式
        self.words=self.mydb.select(f"select rowid,* from words where insert_date='{date}'")
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0): 
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)
            
    def today_exam(self):
        self.words=self.mydb.select(f"select rowid,* from words where insert_date='{self.datetime}'")
        if self.checkBox_random.isChecked():
            # shuffle(self.words)
            self.words=self.words[::-1]
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0):
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHiddfen(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)

    def review_words(self):
        # 1． 第一个记忆周期：5分钟
        # 2． 第二个记忆周期：30分钟
        # 3． 第三个记忆周期：12小时
        # 4． 第四个记忆周期：1天
        # 5． 第五个记忆周期：2天
        # 6． 第六个记忆周期：4天
        # 7． 第七个记忆周期：7天
        # 8． 第八个记忆周期i：15天
        date1=str(datetime.date.today()-datetime.timedelta(days=1))
        date2=str(datetime.date.today()-datetime.timedelta(days=2))
        date3=str(datetime.date.today()-datetime.timedelta(days=4))
        date4=str(datetime.date.today()-datetime.timedelta(days=7))
        date5=str(datetime.date.today()-datetime.timedelta(days=15))
        self.words=self.mydb.select(f"select rowid,* from words where insert_date='{date1}' or insert_date='{date2}' or insert_date='{date3}'  or insert_date='{date4}'  or insert_date='{date5}'")
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0):
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)

    def random_exam(self):
        random_list=[]
        for i in range(1,51):
            random_list.append(randrange(1,self.all_words_num+1))
        sql="select rowid,* from words where "
        for i in random_list:
            sql+=f"rowid={i} or "
        sql=sql[:-3]
        self.words=self.mydb.select(sql)
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0):
                    self.remove_forget_pushButton.setHidden(False)
                    self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)

    def forgoten_exam(self):
        self.remove_forget_pushButton.setHidden(False)
        self.forget_pushButton.setHidden(False)
        self.words=self.mydb.select(f"select rowid,* from words where wrong_times != 0 order by 6 desc")
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(2)
            self.words_index=0
            self.part_of_speech_label.setText(self.words[self.words_index][3])
            self.exam_chinese_label.setText(self.words[self.words_index][2])
            self.word_num=len(self.words)
            self.progress_label.setText(f"{self.words_index}/{self.word_num}")
            self.exam_english_lable.setText("")
            self.forget_label.setText("")
            if (self.words[self.words_index][5] !=0):
                self.remove_forget_pushButton.setHidden(False)
                self.forget_pushButton.setHidden(False)
            else:
                self.remove_forget_pushButton.setHidden(True)
                self.forget_pushButton.setHidden(False)

    def changepage_main(self):
        self.Stacked.setCurrentIndex(0)

    def changepage_add(self):
        self.english_input_edit.setText("random")
        self.display_online()
        self.Stacked.setCurrentIndex(1)

    def changepage_update(self):
        self.Stacked.setCurrentIndex(2)
        self.update_words=self.update_page_search()
        self.update_table.setRowCount(len(self.update_words))
        #######

        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+self.update_words[0][1]+"'")
            # self.play_voice_1.setText(Oxford_data[0][1])
            b64decode(Oxford_data[0][1]).decode()
            self.Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
            # self.Oxford_info_box.setText("aggressive	<font color=red>aggressive</font><br><font color=\"#F17D1F\" size=4>/əˈgresɪv; ə`ɡrɛsɪv/</font> adj<br><font color=green>1</font><br><font color=red>(a) (of people or animals) apt or ready to attack; offensive; quarrelsome （指人或动物）侵略的, 好攻击的, 好寻衅的, 好争吵的</font><br>&nbsp;&nbsp;&nbsp;&nbsp;<font color=blue>dogs trained to be aggressive 训练成攻击型的狗</font><br>&nbsp;&nbsp;&nbsp;&nbsp;<font color=blue>Aggressive nations threaten world peace. 侵略成性的国家威胁世界和平.</font><br><font color=red>(b) (of things or actions) for or of an attack; offensive （指事物或行动）攻击性的</font><br>&nbsp;&nbsp;&nbsp;&nbsp;<font color=blue>aggressive weapons 攻击性的武器.</font><br><font color=green>2 (often approv 常作褒义) forceful; self-assertive 强有力的; 坚持己见的</font><br>&nbsp;&nbsp;&nbsp;&nbsp;<font color=blue>A good salesman must be aggressive if he wants to succeed. 要做个好推销员一定要有闯劲才能成功. </font><br>")
            
        except:
            self.play_voice_1.setText("")
            self.Oxford_info_box.setText("")
        self.selection_word.setText(self.update_words[0][1])
        define_word=self.youdao.main_no_print(self.update_words[0][1],f"select * from words where (english='{self.update_words[0][1]}')")
        # print(phonetic_symbol[0][0])
        self.play_voice_label_1.setText("英 /"+define_word[0][1]+"/")
        self.play_voice_label_2.setText("美 /"+define_word[0][2]+"/")
        self.insert_date.setText("添加日期："+self.update_words[0][4])
        self.words_list.setText("组别名称："+self.update_words[0][6])


        
        display_data="<table><tr>"
        for data in define_word:
            display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
        display_data+="</table>"+data[5].replace("\n","<br>")
        display_data+="<h3>例句</h3>"+b64decode(data[6]).decode()
        
        self.youdao_textBrowswer.setText(display_data)
        self.youdao_textBrowswer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.online_Oxford_info_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.online_youdao_textBoswer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.word_info_table.setRowCount(1)
        newItem = QTableWidgetItem(self.update_words[0][3])
        newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.word_info_table.setItem(0,0,newItem)
        newItem = QTableWidgetItem(self.update_words[0][2])
        self.word_info_table.setItem(0,1,newItem)    

        self.word_info_table.resizeRowsToContents()#自调整高度
        self.tabWidget.setCurrentIndex(2)#切换单词解释界面
        # self.word_info_table.resizeColumnsToContents()#自调整宽度

    def changepage_exam(self):
        self.Stacked.setCurrentIndex(3)
        self.exam_stacked.setCurrentIndex(0)

    def changepage_exam_calendar(self):
        self.exam_stacked.setCurrentIndex(1)
    
    def changepage_exam_main(self):
        self.exam_stacked.setCurrentIndex(0)

    # def back_add_english_widget(self):
    #     self.group=self.list_lineEdit_2.text()
    #     self.list_lineEdit_1.setText(self.group)
    #     self.Add_Stack.setCurrentIndex(0)
    
    # def back_add_frame_to_part_of_speech(self):
    #     self.group=self.list_lineEdit_3.text()
    #     self.list_lineEdit_2.setText(self.group)
    #     self.Add_Stack.setCurrentIndex(1)

    # def change_add_frame_to_part_of_speech(self):
    #     self.group=self.list_lineEdit_1.text()
    #     self.list_lineEdit_2.setText(self.group)
    #     self.Add_Stack.setCurrentIndex(1)

    # def change_add_frame_to_chinese(self):
    #     self.group=self.list_lineEdit_2.text()
    #     self.list_lineEdit_3.setText(self.group)
    #     self.Add_Stack.setCurrentIndex(2)
    #     self.insert_to_add_chinese_table()
    
    # def complete_one(self):
    #     self.group=self.list_lineEdit_3.text()
    #     for ch in range(0,len(self.part_of_speech_dic)):
    #         if (self.add_chinese_input_table_widget.item(ch, 1) == None) or (self.add_chinese_input_table_widget.item(ch, 1).text() == ""):
    #                 msg_box = QMessageBox(QMessageBox.Warning, '警告', '含义不能为空')
    #                 msg_box.exec_()
    #                 return 0
    #         else:
    #             chinese=self.add_chinese_input_table_widget.item(ch, 1).text()
    #             self.part_of_speech_dic[self.add_chinese_input_table_widget.item(ch, 0).text()]=chinese

    #     english=self.add_english_input_edit.text()
    #     if self.group == "":
    #         self.group=self.mydb.select("select list from words order by rowid desc;")[0][0]
    #     for (posd,ch) in self.part_of_speech_dic.items():
    #         self.mydb.insert(english,ch,posd,self.datetime,0,self.group)
    #     self.add_english_input_edit.setText("")
    #     self.clear_add_chinese_table()
    #     self.Add_Stack.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window=mainwindow()
    # from qt_material import apply_stylesheet
    # apply_stylesheet(app, theme='light_amber.xml')
    window.show() 
    sys.exit(app.exec_())