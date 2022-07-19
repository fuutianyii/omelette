# -*- coding: UTF-8 -*-
import sys
import os
import requests
from requests.exceptions import RequestException
import json
import uuid
import hashlib
import time
class youdao_api():
    def __init__(self):
        self.CURRENT_PATH = os.path.abspath(__file__)
        self.CURRENT_PATH = os.path.split(self.CURRENT_PATH)[0]

        self.YOUDAO_API_URL = 'https://openapi.youdao.com/api'
        self.YOUDAO_API_DOC = r'http://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html'

    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def get_result(self,word):
        time_curtime = int(time.time())
        app_id = '004f7cff636359e8' # 这里填应用ID
        app_key = 'ivQSM1YCE6SQo1vqhLcaZWO3MDdHinCF' # 这里填应用密钥
        uu_id = uuid.uuid4()
        sign = hashlib.sha256((app_id + self.truncate(word)  + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()   # sign生成
        data = {
            'q':word,
            'from':"en",
            'to':"zh-CHS",
            'appKey':app_id,
            'salt': uu_id,
            'sign':sign,
            'signType':"v3",
            'curtime':time_curtime,
        }

        try:
            r = requests.post(self.YOUDAO_API_URL, params=data)
            return r.json()
        except RequestException as e:
            print('net error: %s' % e.message)
            sys.exit()


    def main(self,word):
        # youdao=youdao_api()
        result = self.get_result(word)
        
        if 'basic' in result:
            basic = result['basic']
            explains = basic['explains']
            if len(explains) > 0:
                for e in explains:
                    if e.find(".") != -1:
                        print("词性：",e[:e.find(".")])
                        print("词意：",e[e.find(" ")+1:])
                print('')
        
            if 'uk-phonetic' in basic:
                print('英式发音:' + basic['uk-phonetic']) 
            if 'us-phonetic' in basic:
                print('美式发音:' + basic['us-phonetic']) 
            print('')

        if 'web' in result:
            print('网络翻译：')
            for e in result['web']:
                print('{}: {}'.format(e['key'], str(e['value']).replace("[","").replace("]","").replace("\'","")))
            print('')


    def main_no_print(self,word):
        # youdao=youdao_api()
        word_dict={}
        result = self.get_result(word)
        
        if 'basic' in result:
            basic_dict={}
            basic = result['basic']
            explains = basic['explains']
            if len(explains) > 0:
                for e in explains:
                    if e.find(".") != -1:
                        # print("词性：",e[:e.find(".")])
                        # print("词意：",e[e.find(" ")+1:])
                        basic_dict[e[:e.find(".")]]=e[e.find(" ")+1:]
            word_dict['base_dict']=basic_dict
            phonetic_dict={}
            if 'uk-phonetic' in basic:
                phonetic_dict['uk-phonetic']=basic['uk-phonetic']
                # print('英式发音:' + basic['uk-phonetic']) 
            if 'us-phonetic' in basic:
                phonetic_dict['us-phonetic']=basic['us-phonetic']
                # print('美式发音:' + basic['us-phonetic'])
            word_dict['phonetic']=phonetic_dict
        web_dict={}
        if 'web' in result:
            # print('网络翻译：')
            for e in result['web']:
                web_dict[e['key']]=str(e['value']).replace("[","").replace("]","").replace("\'","")
                # print('{}: {}'.format(e['key'], str(e['value']).replace("[","").replace("]","").replace("\'","")))
        word_dict["web"]=web_dict
        # print(word_dict)
        return word_dict
        
if __name__ == '__main__':
    youdao=youdao_api()
    word=youdao.main_no_print("twin")
    
        # n = input("input:")
        # youdao=youdao_api()
        # result = youdao.get_result(n)
        
        # if 'basic' in result:
        #     basic = result['basic']
        #     explains = basic['explains']
        #     if len(explains) > 0:
        #         for e in explains:
        #             if e.find(".") != -1:
        #                 print("词性：",e[:e.find(".")])
        #                 print("词意：",e[e.find(" ")+1:])
        #         print('')
        
        #     if 'uk-phonetic' in basic:
        #         print('英式发音:' + basic['uk-phonetic']) 
        #     if 'us-phonetic' in basic:
        #         print('美式发音:' + basic['us-phonetic']) 
        #     print('')

        # if 'web' in result:
        #     print('网络翻译：')
        #     for e in result['web']:
        #         print('{}: {}'.format(e['key'], str(e['value']).replace("[","").replace("]","").replace("\'","")))
        #     print('')