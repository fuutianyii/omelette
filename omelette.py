#!python3.8
#-*- coding: utf-8 -*-
'''
Author: fuutianyii
Date: 2022-09-09 15:54:42
LastEditors: fuutianyii
LastEditTime: 2022-09-28 15:19:40
github: https://github.com/fuutianyii
mail: fuutianyii@gmail.com
QQ: 1587873181
'''
import Ui_UI
import db
import youdao
import sys
import datetime
from re import compile,findall
from time import sleep  
from os import getcwd,path,chdir
from requests import get
from time import localtime,strftime
from random import randrange
from base64 import b64decode
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem,QMessageBox,QAbstractItemView,QGraphicsBlurEffect,QGraphicsBlurEffect
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer 
from PyQt5.QtCore import Qt,QUrl 
from PyQt5.QtGui import QPixmap,QIcon,QFont,QFontDatabase
# chdir("/Users/fty/python/omelette")


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
        self.forget_word=[]
        # self.blur(self.hello_picture)#实现毛玻璃
        
        
        
    def blur(self,pic,radius):
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(radius)
        blur.setBlurHints(QGraphicsBlurEffect.QualityHint)
        # self.setGraphicsEffect(blur)
        pic.setGraphicsEffect(blur)
        
        ######
    def  clear_add_chinese_table(self):
        for i in range(1,self.lens+1):
            self.add_chinese_input_table_widget.removeRow(0)
            self.lens=1

    def autostart(self):
        self.Stacked.setCurrentIndex(0)

    def read_ui(self,filename):
        f=open("ui/"+filename+".uif","rb")
        return f.read().decode()
    
    def sort_list(self,my_list):##对数据进行净化和排序
        for i in range(0,len(my_list)):
            my_list[i]=my_list[i][0]
        def sort_key(s):
            re_digits = compile(r'(\d+)')
            pieces = re_digits.split(s)  # 切成数字与非数字
            pieces[1::2] = map(int, pieces[1::2])  # 将数字部分转成整数
            return pieces
        my_list.sort(key=sort_key)
        print(my_list)
        return my_list
        
    
    def remake_ui(self):
        #使用本地字体
        fontDb = QFontDatabase()
        fontID = fontDb.addApplicationFont("SourceHanSansCN-Medium.otf")  # 此处的路径为qrc文件中的字体路径
        fontFamilies = fontDb.applicationFontFamilies(fontID)
        print(fontFamilies)
        if fontFamilies!=[]:
            font=QFont(fontFamilies[0])
            font=QFont("Microsoft YaHei")
        else:
            print("Have no the font family")
            font=QFont("Source Han Sans CN Medium")
        self.date_text.setFont(font)
        self.date_text.setFont(font)
        self.sentence_text_chinese.setFont(font)
        self.sentence_text_english.setFont(font)
        self.seach_input_edit.setFont(font)
        self.left_first_button.setFont(font)
        self.left_third_button.setFont(font)
        self.left_forth_button.setFont(font)
        self.english_input_edit.setFont(font)
        self.online_youdao_textBoswer.setFont(font)
        self.online_Oxford_info_box.setFont(font)
        self.search_edit.setFont(font)
        self.selection_word.setFont(font)
        self.selection_word_2.setFont(font)
        self.insert_date.setFont(font)
        self.insert_date_2.setFont(font)
        self.words_list.setFont(font)
        self.words_list_2.setFont(font)
        self.tabWidget.setFont(font)
        self.tabWidget_2.setFont(font)
        self.youdao_textBrowswer.setFont(font)
        self.youdao_textBrowswer_2.setFont(font)
        self.Oxford_info_box.setFont(font)
        self.Oxford_info_box_2.setFont(font)
        self.exam_chinese_label.setFont(font)
        self.part_of_speech_label.setFont(font)
        self.exam_english_lable.setFont(font)
        self.word_info.setFont(font)
        self.word_info_2.setFont(font)
        self.update_table.setFont(font)
        self.update_table_2.setFont(font)
        self.filter_list_comboBox.setFont(font)
        self.filter_date_comboBox.setFont(font)
        self.start_exam.setFont(font)
        self.search_forget_words.setFont(font)
        
        ####调整窗口大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        print("Screen height {}".format(self.screenheight))
        print("Screen width {}".format(self.screenwidth))#938*580
        print(self.screenwidth//2,self.screenheight//2)
        if self.screenheight//2 <580:
            self.resize(self.screenwidth//2,self.screenheight//2)
        else:
            self.resize(900,580)

        self.Stacked.setStyleSheet("QStackedWidget{background:rgba(235,235,235,1)}")
        self.leftframe.setStyleSheet("background-image:none;background:rgba(235,235,235,1);}")
        self.leftframe_top.setStyleSheet("background-image:none;background:rgba(235,235,235,0);}")
        self.homepage_left.setStyleSheet("#homepage_left{background:rgba(255,255,255,0);}")
        self.english_input_edit.setStyleSheet("border: none;border-radius: 15px;font-size:40px;padding-left:20px;background:rgba(255,255,255,1)")
        self.homepage_right.setStyleSheet("background:none;")
        self.verticalFrame.setStyleSheet(self.read_ui("all_frame"))
        self.add_english_input_frame.setStyleSheet(self.read_ui("all_frame"))
        self.frame_12.setStyleSheet(self.read_ui("all_frame"))
        self.frame_13.setStyleSheet(self.read_ui("all_frame"))
        self.search_frame.setStyleSheet(self.read_ui("all_frame"))
        self.frame_5.setStyleSheet(self.read_ui("all_frame"))
        self.search_date_time_frame.setStyleSheet(self.read_ui("all_frame"))
        self.frame_8.setStyleSheet(self.read_ui("all_frame"))
        self.frame_6.setStyleSheet(self.read_ui("all_frame"))
        self.frame_11.setStyleSheet(self.read_ui("all_frame"))
        self.frame_exam_today.setStyleSheet(self.read_ui("all_frame"))
        self.frame_review_words.setStyleSheet(self.read_ui("all_frame"))
        self.frame_radom_exam.setStyleSheet(self.read_ui("all_frame"))
        self.frame_review_Forgotten.setStyleSheet(self.read_ui("all_frame"))
        self.option_frame.setStyleSheet(self.read_ui("all_frame"))
        self.frame_9.setStyleSheet(self.read_ui("all_frame"))
        self.frame_2.setStyleSheet(self.read_ui("all_frame"))
        self.frame_3.setStyleSheet(self.read_ui("all_frame"))
        self.frame_4.setStyleSheet(self.read_ui("all_frame"))
        self.frame_7.setStyleSheet(self.read_ui("all_frame"))
        self.foetget_frame.setStyleSheet(self.read_ui("all_frame"))
        
        
        #测试页中文
        self.exam_chinese_label.setStyleSheet(self.read_ui("exam_chinese_label"))
        
        #词性
        self.part_of_speech_label.setStyleSheet(self.read_ui("exam_chinese_label"))
        
        #单词本页单词列表
        self.Stacked.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(2)
        self.update_table.setStyleSheet(self.read_ui("update_table"))
        self.update_table_2.setStyleSheet(self.read_ui("update_table"))
        
        
        #单词本页的筛选器
        self.filter_list_comboBox.addItem("全部分组")
        self.all_lists=self.sort_list(self.all_lists)
        for list_one in self.all_lists:
            self.filter_list_comboBox.addItem(list_one)
        self.filter_list_comboBox.setStyleSheet(self.read_ui("all_comboBox"))
        self.all_insert_dates=self.sort_list(self.all_insert_dates)
        self.filter_date_comboBox.addItem("全部时间")
        for date in self.all_insert_dates:
            self.filter_date_comboBox.addItem(date)
        self.filter_date_comboBox.setStyleSheet(self.read_ui("all_comboBox"))
        
        #左侧四个功能按键的frame
        # self.leftframe.setStyleSheet(self.read_ui("leftframe"))
        
        #按钮
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/home_light"), QIcon.Normal, QIcon.Off)
        self.left_first_button.setIcon(icon)
        self.left_first_button.setStyleSheet(self.read_ui("button"))

        # icon = QIcon()
        # icon.addPixmap(QPixmap("ico/search.png"), QIcon.Normal, QIcon.Off)
        # self.left_second_button.setIcon(icon)
        # self.left_second_button.setStyleSheet(self.read_ui("button"))

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star_book.png"), QIcon.Normal, QIcon.Off)
        self.left_third_button.setIcon(icon)
        self.left_third_button.setStyleSheet(self.read_ui("button"))

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting.png"), QIcon.Normal, QIcon.Off)
        self.left_forth_button.setIcon(icon)
        self.left_forth_button.setStyleSheet(self.read_ui("button"))
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting.png"), QIcon.Normal, QIcon.Off)
        self.more_functions.setIcon(icon)
        self.more_functions.setStyleSheet(self.read_ui("button"))
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/sync.png"), QIcon.Normal, QIcon.Off)
        self.Sync.setIcon(icon)
        self.Sync.setStyleSheet(self.read_ui("button"))
    
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/sync.png"), QIcon.Normal, QIcon.Off)
        self.Sync.setIcon(icon)
        self.Sync.setStyleSheet(self.read_ui("button"))
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/start.png"), QIcon.Normal, QIcon.Off)
        self.start_exam.setIcon(icon)
        self.start_exam.setStyleSheet(self.read_ui("button"))

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/forget.png"), QIcon.Normal, QIcon.Off)
        self.search_forget_words.setIcon(icon)
        self.search_forget_words.setStyleSheet(self.read_ui("button"))

        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star.png"), QIcon.Normal, QIcon.Off)
        self.star.setIcon(icon)
        self.star.setStyleSheet(self.read_ui("button"))
        
        #主页搜索
        self.seach_input_edit.setPlaceholderText("搜索单词")
        self.seach_input_edit.setStyleSheet(self.read_ui("search_input_edit"))
        
        #主页左侧frame
        # self.homepage_left.setStyleSheet(self.read_ui("homepage_left"))
        
        #测试中文居中
        self.forget_label.setAlignment(Qt.AlignCenter)

        #主页时间显示
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
            
      
      

        
        
        self.date_text.setText(month +" "+time_list[2])
        self.date_text.setStyleSheet(self.read_ui("date_text"))
        

        self.insert_date.setStyleSheet(self.read_ui("grey_info"))
        self.words_list.setStyleSheet(self.read_ui("grey_info"))
        self.insert_date_2.setStyleSheet(self.read_ui("grey_info"))
        self.words_list_2.setStyleSheet(self.read_ui("grey_info"))
        
        self.list_line.setStyleSheet(self.read_ui("white_edit"))
        self.list_line.setPlaceholderText("输入类名")
        
        self.search_edit.setStyleSheet(self.read_ui("white_edit"))
        self.search_edit.setPlaceholderText("搜索单词")
        
        

        
        #主页图片及每日一句
        if (path.exists("daily/"+month+time_list[2]+"bg.jpg")):
            self.hello_picture.setStyleSheet("QLabel{background-image:url(\"daily/"+month+time_list[2]+"bg.jpg\");background-position: right;background-repeat: no-repeat;}")
            f=open("daily/"+month+time_list[2]+"en.txt","rb")
            self.sentence_text_english.setText(f.read().decode())
            f.close()
            f=open("daily/"+month+time_list[2]+"ch.txt","rb")
            self.sentence_text_chinese.setText(f.read().decode())
            f.close()
            self.sentence_text_english.setStyleSheet("QLabel{font-size:20px;margin-bottom:10px;}")
            self.sentence_text_english.setWordWrap(True)
            self.sentence_text_chinese.setStyleSheet("QLabel{font-size:20px;margin-bottom:10px;}")
            self.sentence_text_chinese.setWordWrap(True)
        else:
            api_data=get("http://open.iciba.com/dsapi/").text
            c=compile(r'{".*?":".*?",".*?":"(.*?)",".*?":"(.*?)","note":"(.*?)",".*?":".*?",".*?":".*?",".*?":".*?",".*?":"(.*?)"')
            api=findall(c,api_data)
            print(api)
            s=get(api[0][3])
            f=open("daily/"+month+time_list[2]+"bg.jpg","wb")
            f.write(s.content)
            f.close()
            f=open("daily/"+month+time_list[2]+"en.txt","wb")
            f.write(api[0][1].encode())
            f.close()
            f=open("daily/"+month+time_list[2]+"ch.txt","wb")
            f.write(api[0][2].encode())
            f.close()
            
            self.hello_picture.setStyleSheet("QLabel{background-image:url(\"daily/"+month+time_list[2]+"bg.jpg\");background-position: right;background-repeat: no-repeat;}")
            self.sentence_text_english.setText(api[0][1])
            self.sentence_text_chinese.setText(api[0][2])
            self.sentence_text_english.setStyleSheet("QLabel{font-size:20px;margin-bottom:10px;}")
            self.sentence_text_english.setWordWrap(True)
            self.sentence_text_chinese.setStyleSheet("QLabel{font-size:20px;margin-bottom:10px;}")
            self.sentence_text_chinese.setWordWrap(True)
        
        self.online_youdao_textBoswer.setStyleSheet(self.read_ui("QTextBrowser"))
        self.Oxford_info_box.setStyleSheet(self.read_ui("QTextBrowser"))
        self.Oxford_info_box_2.setStyleSheet(self.read_ui("QTextBrowser"))
        self.online_Oxford_info_box.setStyleSheet(self.read_ui("QTextBrowser"))
        self.youdao_textBrowswer.setStyleSheet(self.read_ui("QTextBrowser"))
        self.youdao_textBrowswer_2.setStyleSheet(self.read_ui("QTextBrowser"))
        self.word_info.setStyleSheet(self.read_ui("QTextBrowser"))
        self.word_info_2.setStyleSheet(self.read_ui("QTextBrowser"))
        self.word_info.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.word_info_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.online_youdao_textBoswer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Oxford_info_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Oxford_info_box_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.online_Oxford_info_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.youdao_textBrowswer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.youdao_textBrowswer_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.word_info.setTextInteractionFlags(Qt.NoTextInteraction)
        self.word_info_2.setTextInteractionFlags(Qt.NoTextInteraction)
        self.online_youdao_textBoswer.setTextInteractionFlags(Qt.NoTextInteraction)
        self.youdao_textBrowswer.setTextInteractionFlags(Qt.NoTextInteraction)
        self.youdao_textBrowswer_2.setTextInteractionFlags(Qt.NoTextInteraction)
        self.Oxford_info_box.setTextInteractionFlags(Qt.NoTextInteraction)
        self.Oxford_info_box_2.setTextInteractionFlags(Qt.NoTextInteraction)
        self.online_Oxford_info_box.setTextInteractionFlags(Qt.NoTextInteraction)
        self.youdao_textBrowswer.setTextInteractionFlags(Qt.NoTextInteraction)
        self.youdao_textBrowswer_2.setTextInteractionFlags(Qt.NoTextInteraction)

        self.update_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table.setFocusPolicy(Qt.NoFocus)
        #取消虚线框
        self.update_table.setShowGrid(False)
        #取消网格线
        self.update_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #不可写
        self.update_table.horizontalHeader().setVisible(False)
        #self.update_table.verticalHeader().setVisible(False)
        self.update_table.setColumnCount(1)
        self.update_table.setRowCount(self.update_table.rowCount()+1)
        self.update_table.setColumnWidth(0,130)

        self.update_table_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table_2.setFocusPolicy(Qt.NoFocus)
        #取消虚线框
        self.update_table_2.setShowGrid(False)
        #取消网格线
        self.update_table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #不可写
        self.update_table_2.horizontalHeader().setVisible(False)
        #self.update_table.verticalHeader().setVisible(False)
        self.update_table_2.setColumnCount(1)
        self.update_table_2.setRowCount(self.update_table_2.rowCount()+1)
        self.update_table_2.setColumnWidth(0,130)


        icon = QIcon()
        icon.addPixmap(QPixmap("ico/voice.png"), QIcon.Normal, QIcon.Off)
        self.play_voice_1.setIcon(icon)
        self.play_voice_1.setStyleSheet(self.read_ui("play_voice"))
        self.play_voice_1.adjustSize()
        self.play_voice_2.setIcon(icon)
        self.play_voice_2.setStyleSheet(self.read_ui("play_voice"))
        self.play_voice_2.adjustSize()
        
        self.play_voice_3.setIcon(icon)
        self.play_voice_3.setStyleSheet(self.read_ui("play_voice"))
        self.play_voice_3.adjustSize()
        self.play_voice_4.setIcon(icon)
        self.play_voice_4.setStyleSheet(self.read_ui("play_voice"))
        self.play_voice_4.adjustSize()
        
        self.online_play_voice_1.setIcon(icon)
        self.online_play_voice_1.setStyleSheet(self.read_ui("play_voice"))
        self.online_play_voice_1.adjustSize()
        self.online_play_voice_2.setIcon(icon)
        self.online_play_voice_2.setStyleSheet(self.read_ui("play_voice"))
        self.online_play_voice_2.adjustSize()
        
        self.tabWidget.setStyleSheet("QTabWidget{border:none;}QTabWidget::pane{border:none;}QTabWidget::tab-bar {left: 5px;}QTabBar::tab {border-bottom-color: #C2C7CB;border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 60px;padding: 2px;}QTabBar::tab:selected{color:rgba(0,0,0,1);}QTabBar::tab:selected{background:rgba(255,255,255,1);}QTabBar::tab:!selected{margin-top:5px;}/*四个下属界面*/#tab,#tab_2,#tab_3,#tab_4{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454)border-radius:6px;}")
        self.tabWidget_2.setStyleSheet("QTabWidget{border:none;}QTabWidget::pane{border:none;}QTabWidget::tab-bar {left: 5px;}QTabBar::tab {border-bottom-color: #C2C7CB;border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 60px;padding: 2px;}QTabBar::tab:selected{color:rgba(0,0,0,1);}QTabBar::tab:selected{background:rgba(255,255,255,1);}QTabBar::tab:!selected{margin-top:5px;}/*四个下属界面*/#tab,#tab_2,#tab_3,#tab_4{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454)border-radius:6px;}")
        self.online.setStyleSheet("QTabWidget{border:none;}QTabWidget::pane{border:none;}QTabWidget::tab-bar {left: 5px;}QTabBar::tab {border-bottom-color: #C2C7CB;border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 60px;padding: 2px;}QTabBar::tab:selected{color:rgba(0,0,0,1);}QTabBar::tab:selected{background:rgba(255,255,255,1);}QTabBar::tab:!selected{margin-top:5px;}/*四个下属界面*/#tab,#tab_2,#tab_3,#tab_4{background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #626262,stop:1 #545454)border-radius:6px;}")
        QApplication.processEvents()
        
        
  
        
        # op = QGraphicsOpacityEffect()
        # op.setOpacity(0.5)
        # self.hello_picture.setGraphicsEffect(op)


    def condef(self):
        self.english_input_edit.returnPressed.connect(self.display_online)
        self.seach_input_edit.returnPressed.connect(self.homepage_to_search)
        self.left_first_button.clicked.connect(self.changepage_main)
        # self.left_second_button.clicked.connect(self.changepage_add)
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
        # self.exam_calendarWidget.clicked.connect(self.start_choose_exam)
        # self.update.clicked.connect(self.update_all_words)
        self.forget_pushButton.clicked.connect(self.display_forget)
        # self.delete_choose.clicked.connect(self.delete_words)
        self.exam_english_lable.returnPressed.connect(self.exam_submit)
        self.exam_today_button.clicked.connect(self.today_exam)
        self.review_words_button.clicked.connect(self.review_words)
        self.reset_forget_button.clicked.connect(self.reset_forget)
        self.radom_exam_button.clicked.connect(self.random_exam)
        self.review_Forgotten_button.clicked.connect(self.forgoten_exam)
        self.remove_forget_pushButton.clicked.connect(self.reset_wrong_times)
        self.update_table.itemClicked.connect(self.show_defined_selection)
        self.update_table_2.itemClicked.connect(self.show_defined_selection_2)
        self.play_voice_1.clicked.connect(self.play_the_word_uk)
        self.play_voice_2.clicked.connect(self.play_the_word_us)
        
        self.play_voice_3.clicked.connect(self.play_the_word_uk_2)
        self.play_voice_4.clicked.connect(self.play_the_word_us_2)
        self.start_exam.clicked.connect(self.exam_choose_words)
        
        
        # self.filter_list_comboBox.currentIndexChanged.connect(self.update_page_search)
        # self.filter_date_comboBox.currentIndexChanged.connect(self.update_page_search)
        self.filter_list_comboBox.currentIndexChanged.connect(self.filter_list)
        self.filter_date_comboBox.currentIndexChanged.connect(self.filter_date)
        self.search_forget_words.clicked.connect(self.select_forget_words)
        
        self.Sync.clicked.connect(self.reverse_words_list)
        
        
        self.online_play_voice_1.clicked.connect(self.online_play_the_word_uk)
        self.online_play_voice_2.clicked.connect(self.online_play_the_word_us)


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
        self.online_search(self.seach_input_edit)

    def display_online(self):
        self.online_search(self.english_input_edit)
    
    def online_search(self,edit):
        if edit.text()=="":
            return 0
        self.Stacked.setCurrentIndex(1)
        self.english_input_edit.setText(edit.text())
        self.online_dict=self.youdao.main_no_print_online(edit.text())
        if self.online_dict != []:
            self.online_play_voice_1.setText(self.online_dict[0][1]+"  ")
            self.online_play_voice_2.setText(self.online_dict[0][2]+"  ")
            display_data=""
            if self.online_dict[0][3]!="":
                display_data="<table><tr>"
                for data in self.online_dict:
                    display_data+="<td>"+data[3]+"</td><td> "+data[4]+"</td></tr><tr>"
                display_data+="</table>"+data[5].replace("\n","<br>")
            if self.online_dict[0][5]!="":
                display_data+=self.online_dict[0][5].replace("\n","<br>")
            if self.online_dict[0][6]!="":
                display_data+="<h2>例句</h2>"+self.online_dict[0][6]
            self.online_youdao_textBoswer.setText(display_data)

            Oxford_data=self.myOxford.select("select * from words where english='"+edit.text()+"'")
            
            if (Oxford_data != "") and (Oxford_data != []):
                b64decode(Oxford_data[0][1]).decode()
                self.online_Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
            else:
                self.online_Oxford_info_box.setText("暂无数据")
            
            
            search=f"select english from words where english='{edit.text()}'"
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
        else:
            self.online_youdao_textBoswer.setText("暂无数据")
            self.online_Oxford_info_box.setText("暂无数据")
        QApplication.processEvents()
    
    def get_all_insert_date(self):
        search="select insert_date From words Group By insert_date;"
        self.all_insert_dates=self.mydb.select(search)

    def get_all_list(self):
        search="select list From words Group By list;"
        self.all_lists=self.mydb.select(search)

    def online_play_the_word_uk(self):
        self.online_play(self.english_input_edit.text(),1)
    def online_play_the_word_us(self):
        self.online_play(self.english_input_edit.text(),2)
        
    def play_the_word_uk(self):
        self.play(self.selection_word.text(),1)
    
    def play_the_word_us(self):
        self.play(self.selection_word.text(),2)
        
    def play_the_word_uk_2(self):
        self.play(self.selection_word_2.text(),1)
    
    def play_the_word_us_2(self):
        self.play(self.selection_word_2.text(),2)

    def show_defined_selection(self,Item):
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+Item.text()+"'")
            b64decode(Oxford_data[0][1]).decode()
            self.Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.Oxford_info_box.setText("暂无数据")
        define_word=self.youdao.main_no_print(Item.text(),f"select * from words where (english='{Item.text()}')")
        # print(phonetic_symbol[0][0])


        self.selection_word.setText(Item.text())
        self.insert_date.setText("添加日期："+self.update_words[self.update_table.currentRow()][4])
        self.words_list.setText("组别名称："+self.update_words[self.update_table.currentRow()][6])

        self.word_info.setText("<table><tr><td><b>"+self.update_words[self.update_table.currentRow()][3]+"</b>.&nbsp;&nbsp;</td><td> "+self.update_words[self.update_table.currentRow()][2]+"</td></tr><tr>")
        display_data=""
        if len(define_word)!=0:
            self.play_voice_1.setText("英 /"+define_word[0][1]+"/")
            self.play_voice_2.setText("美 /"+define_word[0][2]+"/")
            
            if define_word[0][3] != "":
                display_data="<table><tr>"
                for data in define_word:
                        display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
                display_data+="</table>"
            if define_word[0][5] != "":
                display_data+=define_word[0][5].replace("\n","<br>")
            if b64decode(define_word[0][6]).decode() != "暂无例句":
                display_data+="<h3>例句</h3>"+b64decode(define_word[0][6]).decode()
        self.youdao_textBrowswer.setText(display_data)

    def show_defined_selection_2(self,Item):
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+Item.text()+"'")
            b64decode(Oxford_data[0][1]).decode()
            self.Oxford_info_box_2.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.Oxford_info_box_2.setText("暂无数据")
        define_word=self.youdao.main_no_print(Item.text(),f"select * from words where (english='{Item.text()}')")
        # print(phonetic_symbol[0][0])
        self.play_voice_3.setText("英 /"+define_word[0][1]+"/")
        self.play_voice_4.setText("美 /"+define_word[0][2]+"/")

        self.selection_word_2.setText(Item.text())
        self.insert_date_2.setText("添加日期："+self.forget_word[self.update_table_2.currentRow()][4])
        self.words_list_2.setText("组别名称："+self.forget_word[self.update_table_2.currentRow()][6])

        self.word_info_2.setText("<table><tr><td><b>"+self.forget_word[self.update_table_2.currentRow()][3]+"</b>.&nbsp;&nbsp;</td><td> "+self.forget_word[self.update_table_2.currentRow()][2]+"</td></tr><tr>")
        
        display_data=""
        if define_word[0][3] != "":
            display_data="<table><tr>"
            for data in define_word:
                    display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
            display_data+="</table>"
        if define_word[0][5] != "":
            display_data+=define_word[0][5].replace("\n","<br>")
        if b64decode(define_word[0][6]).decode() != "暂无例句":
            display_data+="<h3>例句</h3>"+b64decode(define_word[0][6]).decode()
        self.youdao_textBrowswer_2.setText(display_data)
            
    def exam_choose_words(self):
        if len(self.update_words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到单词')
            msg_box.exec_()
        else:
            self.changepage_exam()
            self.words=self.update_words
            if self.checkBox_random.isChecked():
                self.words=self.words[::-1]
            self.exam_stacked.setCurrentIndex(1)
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
            self.update_table.setRowCount(self.update_table.rowCount()+1)
            newItem = QTableWidgetItem(items[1])
            self.update_table.setItem(self.update_table.rowCount()-1,0,newItem)

    def reverse_words_list(self):
        for i in range(0,self.update_table.rowCount()+1):
            self.update_table.removeRow(0)
            self.lens=1
        
        
        self.update_words=self.update_words[::-1]
        for items in self.update_words:
            self.update_table.setRowCount(self.update_table.rowCount()+1)
            newItem = QTableWidgetItem(items[1])
            self.update_table.setItem(self.update_table.rowCount()-1,0,newItem)

    def filter_date(self,index):
        date=self.all_insert_dates[index-1]
        if index==0:
            search=f"select rowid,* from words where insert_date!=''"
            self.date="全部时间"
        else:
            self.date=date
            if self.list=="全部分组":
                search=f"select rowid,* from words where insert_date='{date}'"
            else:
                search=f"select rowid,* from words where insert_date='{date}' and  list='{self.list}'"
        print(search)
        self.update_words=self.mydb.select(search)
        self.update_table.setRowCount(len(self.update_words))
        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            print(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)

    def filter_list(self,index):
        list_one=self.all_lists[index-1]
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
                mp3_path=getcwd().replace("\\", "/")+f"\\mp3\\voice_{word}_{type}.mp3".replace("\\", "/")
                url = QUrl.fromLocalFile(mp3_path)
                content = QMediaContent(url)  # 加载音乐
                self.player.setMedia(content)     # 关联 QMediaPlayer控件与音乐地址
                self.player.play()                          # 播放
            else:
                self.getmp3(word)
                mp3_path=getcwd().replace("\\", "/")+f"\\mp3\\voice_{word}_{type}.mp3".replace("\\", "/")
                print(mp3_path)
                url = QUrl.fromLocalFile(mp3_path)
                content = QMediaContent(url)  # 加载音乐
                self.player.setMedia(content)     # 关联 QMediaPlayer控件与音乐地址
                self.player.play()                          # 播放
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '播放失败')
            msg_box.exec_()

    def online_play(self,word,type):
        respond=get(f"https://dict.youdao.com/dictvoice?audio={word}&type={type}")
        if respond.status_code == 200:
            data=respond.content
            w = open(f"mp3/online_{type}.mp3","wb") 
            w.write(data)
            w.close()
        mp3_path=getcwd().replace("\\", "/")+"/mp3/online.mp3"
        url=QUrl.fromLocalFile(mp3_path)
        content = QMediaContent(url)  # 加载音乐
        self.player.setMedia(content)     # 关联 QMediaPlayer控件与音乐地址
        self.player.play()                          # 播放
    
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
            self.words_index+=1
            self.exam_english_lable.setStyleSheet('''QWidget{background-color:#66FFCC;}''')
            QApplication.processEvents()#刷新样式
            self.exam_english_lable.setText("")
            if self.words_index==self.word_num:
                self.review_examined()
                return 0
            english=self.words[self.words_index][1]
            if self.checkBox_voice.isChecked():
                self.play(english,1)
                sleep(1)
            self.exam_change()
        else:
            self.exam_english_lable.setStyleSheet('''QWidget{background-color:#FFB6C1;}''')
            self.exam_english_lable.setText("")
    
    def review_examined(self):#######
        if len(self.forget_word)!= 0:
            self.exam_stacked.setCurrentIndex(2)
            self.update_table_2.setRowCount(len(self.forget_word))
            for items in range(0,len(self.forget_word)):
                newItem = QTableWidgetItem(self.forget_word[items][1])
                self.update_table_2.setItem(items,0,newItem)
            try:
                Oxford_data=self.myOxford.select("select * from words where english='"+self.forget_word[0][1]+"'")
                print("select * from words where english='"+self.forget_word[0][1]+"'")
                self.Oxford_info_box_2.setText(b64decode(Oxford_data[0][1]).decode())
            except:
                self.Oxford_info_box_2.setText("")
                

            self.selection_word_2.setText(self.forget_word[0][1])
            print(f"select * from words where (english='{self.forget_word[0][1]}')")
            define_word=self.youdao.main_no_print(self.forget_word[0][1],f"select * from words where (english='{self.forget_word[0][1]}')")
            self.play_voice_3.setText("英 /"+define_word[0][1]+"/")
            self.play_voice_4.setText("美 /"+define_word[0][2]+"/")
            self.insert_date_2.setText("添加日期："+self.forget_word[0][4])
            self.words_list_2.setText("组别名称："+self.forget_word[0][6])
            display_data="<table><tr>"
            for data in define_word:
                display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
            display_data+="</table>"+data[5].replace("\n","<br>")
            display_data+="<h3>例句</h3>"+b64decode(data[6]).decode()
            self.youdao_textBrowswer_2.setText(display_data)
            self.word_info_2.setText("<table><tr><td><b>"+self.forget_word[self.update_table_2.currentRow()][3]+"</b>.&nbsp;&nbsp;</td><td> "+self.forget_word[self.update_table_2.currentRow()][2]+"</td></tr><tr>")
        else:
            self.exam_stacked.setCurrentIndex(0)
        
    
    def display_forget(self):
        if self.forgeted == 0:
            english=self.words[self.words_index][1]
            self.forget_word.append(self.words[self.words_index])
            wrong_times=self.mydb.select(f"select wrong_times from words where english='{english}'")[0][0]
            wrong_times=self.mydb.update(f"update words set wrong_times={wrong_times+1} where english='{english}'")
            self.forget_label.setText(self.words[self.words_index][1])
        self.forgeted=1

    def reset_wrong_times(self):
        english=self.words[self.words_index][1]
        wrong_times=self.mydb.update(f"update words set wrong_times=0 where english='{english}'")

    def exam_change(self):
        self.forgeted = 0
        if  len(self.words) == self.words_index:
           self.exam_stacked.setCurrentIndex(1)
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
        
        
                
    # def start_choose_exam(self):
    #     date=str(self.exam_calendarWidget.selectedDate().toPyDate())#获取选中日期并且转为str格式
    #     self.words=self.mydb.select(f"select rowid,* from words where insert_date='{date}'")
    #     if len(self.words)==0:
    #         msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
    #         msg_box.exec_()
    #     else:
    #         self.exam_stacked.setCurrentIndex(2)
    #         self.words_index=0
    #         self.part_of_speech_label.setText(self.words[self.words_index][3])
    #         self.exam_chinese_label.setText(self.words[self.words_index][2])
    #         self.word_num=len(self.words)
    #         self.progress_label.setText(f"{self.words_index}/{self.word_num}")
    #         self.exam_english_lable.setText("")
    #         self.forget_label.setText("")
    #         if (self.words[self.words_index][5] !=0): 
    #             self.remove_forget_pushButton.setHidden(False)
    #             self.forget_pushButton.setHidden(False)
    #         else:
    #             self.remove_forget_pushButton.setHidden(True)
    #             self.forget_pushButton.setHidden(False)
            
    def today_exam(self):
        self.words=self.mydb.select(f"select rowid,* from words where insert_date='{self.datetime}'")
        if self.checkBox_random.isChecked():
            # shuffle(self.words)
            self.words=self.words[::-1]
        if len(self.words)==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '没有获取到words')
            msg_box.exec_()
        else:
            self.exam_stacked.setCurrentIndex(1)
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


    def reset_forget(self):
        self.words=self.mydb.update("update words set wrong_times=0")
        
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
            self.exam_stacked.setCurrentIndex(1)
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
            self.exam_stacked.setCurrentIndex(1)
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
            self.exam_stacked.setCurrentIndex(1)
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
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/home_light"), QIcon.Normal, QIcon.Off)
        self.left_first_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star_book"), QIcon.Normal, QIcon.Off)
        self.left_third_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting"), QIcon.Normal, QIcon.Off)
        self.left_forth_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)




    # def changepage_add(self):
    #     self.english_input_edit.setText("random")
    #     self.display_online()
    #     self.Stacked.setCurrentIndex(1)
    def changepage_update(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/home"), QIcon.Normal, QIcon.Off)
        self.left_first_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star_book_light"), QIcon.Normal, QIcon.Off)
        self.left_third_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting"), QIcon.Normal, QIcon.Off)
        self.left_forth_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        
        self.Stacked.setCurrentIndex(2)
        self.update_words=self.update_page_search()
        self.update_table.setRowCount(len(self.update_words))
        #######

        for items in range(0,len(self.update_words)):
            newItem = QTableWidgetItem(self.update_words[items][1])
            self.update_table.setItem(items,0,newItem)
        try:
            Oxford_data=self.myOxford.select("select * from words where english='"+self.update_words[0][1]+"'")
            print("select * from words where english='"+self.update_words[0][1]+"'")
            self.Oxford_info_box.setText(b64decode(Oxford_data[0][1]).decode())
        except:
            self.Oxford_info_box.setText("")
            
        if len(self.update_words) !=0 :
            self.selection_word.setText(self.update_words[0][1])
            print(f"select * from words where (english='{self.update_words[0][1]}')")
            define_word=self.youdao.main_no_print(self.update_words[0][1],f"select * from words where (english='{self.update_words[0][1]}')")
            self.play_voice_1.setText("英 /"+define_word[0][1]+"/")
            self.play_voice_2.setText("美 /"+define_word[0][2]+"/")
            self.insert_date.setText("添加日期："+self.update_words[0][4])
            self.words_list.setText("组别名称："+self.update_words[0][6])
            display_data="<table><tr>"
            for data in define_word:
                display_data+="<td ><b>"+data[3]+"</b>.&nbsp;&nbsp;</td><td> "+data[4]+"</td></tr><tr>"
            display_data+="</table>"+data[5].replace("\n","<br>")
            display_data+="<h3>例句</h3>"+b64decode(data[6]).decode()
            self.youdao_textBrowswer.setText(display_data)
            self.word_info.setText("<table><tr><td><b>"+self.update_words[self.update_table.currentRow()][3]+"</b>.&nbsp;&nbsp;</td><td> "+self.update_words[self.update_table.currentRow()][2]+"</td></tr><tr>")

    def changepage_exam(self):
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/home"), QIcon.Normal, QIcon.Off)
        self.left_first_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/star_book"), QIcon.Normal, QIcon.Off)
        self.left_third_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        icon = QIcon()
        icon.addPixmap(QPixmap("ico/setting_light"), QIcon.Normal, QIcon.Off)
        self.left_forth_button.setIcon(icon)
        self.Stacked.setCurrentIndex(0)
        
        
        self.left_first_button.setStyleSheet(self.read_ui("button"))
        self.Stacked.setCurrentIndex(3)
        
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
    window.show() 
    sys.exit(app.exec_())
