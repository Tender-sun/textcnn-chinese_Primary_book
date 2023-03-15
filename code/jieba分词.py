import os
import re
import time
import random
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
new_text1 = "F:/分词结果2/n" #最后的两个输出文件夹，n用来存放负类，y存放正类。
new_text2 = "F:/分词结果2/y" #里面存放所有书籍对应的分词结果
def MakeWordsSet(words_file):
    words_set = set()
    with open(words_file, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            word = line.strip().encode('utf-8').decode("utf-8")
            if len(word) > 0 and word not in words_set:  # 去重
                words_set.add(word)
    return words_set
folder_path = 'F:/data2' #存放书籍的文件夹，输入。下面必须分两个文件夹，一个文件夹名为n，一个名为y，存放两类源数据
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
        remove_words = set(line.strip() \
                           for line in open("stopwords_plus.txt", encoding="utf-8").readlines())  # 自定义去除词库
        word_cut = jieba.cut(raw)  # 精确模式，返回的结构是一个可迭代的genertor
        #lcut是返回列表的
        #cut会返回一个generator对象，可以迭代,采用generator时候需要对该数据类型进行转换
        word_cut = list(word_cut)
        for word in word_cut:  # 循环读出每个分词
            if word in remove_words  or word.isdigit():  # 如果不在去除词库中,并且如果是数字的话也要去掉。保留所有的文本信息
                word_cut.remove(word)  # 分词追加到列表
        words = word_cut
        word_list = []
        for word in words:
            if word not in stop_words and not word == ' ' and not word == ' ':
                word_list.append(word)
        all_words_dict = {}
        for word in word_list:
            if word in all_words_dict:
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1
        with open(fresult, 'w' , encoding='UTF-8') as g:
            for word in word_list :
                if not word=='第章':
                #这里可以有很多筛选条件，比如词语的判断，或者只需要长度大于1的词语，以及对出现频数做筛选
                    g.write(str(word))
                    g.write(" ")
                    all_words_dict[word]=0
        with open(fresult, 'r', encoding='UTF-8') as g:
            rr = g.read()
            row = {'label':t,'content':rr}
            df.loc[j] = row
            print(folder,j,' ',file,'done')
        j = j+1
        g.close()
        word_list = []
print('done total')
print(df)
df.to_csv("s5_with字.csv")
#最后存为csv，文件名自定义