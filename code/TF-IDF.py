import os
import re
import jieba.analyse
import time
import random
import jieba.analyse
import jieba
import nltk
import sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import brier_score_loss
jieba.setLogLevel(jieba.logging.INFO)
new_text1 = "F:/分词结果/n"
new_text2 = "F:/分词结果/y"
print("sss")
def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            word = line.strip().encode('utf-8').decode("utf-8")
            if len(word) > 0 and word not in words_set:  # 去重
                words_set.add(word)
    return words_set
folder_path = 'F:/data'
folder_list = os.listdir(folder_path)
data_list = []
class_list = []
# 类间循环
import pandas as pd
df = pd.DataFrame(columns=('label','content'))
stop1 = 'stopwords_plus.txt'
stop2 = 'stopwords_file.txt'
stop_words = MakeWordsSet(stop1)
j=1

for folder in folder_list:
    print(folder)
    new_folder_path = os.path.join(folder_path, folder)
    files = os.listdir(new_folder_path)

    # 类内循环
    for file in files:
        print(file)
        if j > 1000:  # 每类text样本数最多1000
            break
        #print(file)
        if folder == 'n':
            fresult = new_text1 + '/' + file
            t = 0
        else :
            fresult = new_text2 + '/' + file
            t = 1
        with open(os.path.join(new_folder_path, file), 'r', encoding='utf-8') as fp:
           raw1 = fp.read()
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|。|，| |“”|……“”|……“|”“|')  # 定义正则表达式匹配模式
        raw = re.sub(pattern, '', raw1)  # 将符合模式的字符去除
        keywords=jieba.analyse.extract_tags(raw, topK=3000, withWeight=False, allowPOS=())
        remove_words = set(line.strip() \
                           for line in open("stopwords_plus.txt", encoding="utf-8").readlines())  # 自定义去除词库
        print(type(keywords))
        with open(fresult, 'w' , encoding='UTF-8') as g:
            for word in keywords:
                if not word=='第章':
                    g.write(str(word))
                    g.write(" ")
        with open(fresult, 'r', encoding='UTF-8') as g:
            rr = g.read()
            row = {'label':t,'content':rr}
            df.loc[j] = row
            print(folder,j,' ',file,'done')
        j = j+1
        keywords = []
print('done total')
print(df)
df.to_csv("tf-idf-01.csv")