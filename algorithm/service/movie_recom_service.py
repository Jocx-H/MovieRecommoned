#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/5 13:26
@Author : Jocx-H
@File   : movie_recom_service.py
@Desc   :  PyCharm
'''

import json
import numpy as np
import os
import random
import sys
import traceback

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from time import *
from typing import List
from math import sqrt
from operator import itemgetter
from dao import info_dao

MAIN_PATH = os.path.abspath(os.path.dirname(r'.'))
BASE_PATH = os.path.join(MAIN_PATH, 'assets')
DATA_PATH = os.path.join(BASE_PATH, 'data')
RATING_PATH = os.path.join(DATA_PATH, 'ratings.csv')

REC_ITEMS = 24
SIM_ITEMS = 100
MAX_TIMESTAMP = 1537945149

movie_tag = {
    1: 'Action', 2: 'Adventure', 3: 'Animation', 4: 'Children', 5: 'Comedy', 6: 'Fantasy',
    7: 'IMAX', 8: 'Romance', 9: 'Sci-Fi', 10: 'Western', 11: 'Crime', 12: 'Mystery',
    13: 'Drama', 14: 'Thriller', 15: 'War', 16: 'Horror', 17: 'Film-Noir', 18: 'Documentary',
    19: 'Musical', 20: 'Others'
}


class ItemBasedCF:
    def __init__(self, filename):
        """
        初始化参数
        """
        self.user_item = {}
        self.item_sim_matrix = {}
        self.item_popular = {}
        self.movie_type = {}
        self.item_count = 0
        self.filename = filename
        self.user_item_name = "movie_user_item.json"
        self.item_sim_name = "movie_item_sim.json"
        self.movie_type_name = "sorted.json"
        with open(os.path.join(DATA_PATH, self.movie_type_name), "r") as f3:
            self.movie_type = json.load(f3)

        try:
            with open(os.path.join(DATA_PATH, self.user_item_name), "r") as f1:
                self.user_item = json.load(f1)
            with open(os.path.join(DATA_PATH, self.item_sim_name), "r") as f2:
                self.item_sim_matrix = json.load(f2)
        except FileNotFoundError:
            self.get_dataset()
            self.calc_item_sim()
            self.save()

    def perfer_cal(self, score, timestamp):
        """
        综合用户评分、时间戳得到一个综合评分
        param line:数据库中的一行数据
        return:综合评分
        """
        total_sec = 24 * 60 * 60 * 365 * 10
        delta = (MAX_TIMESTAMP - timestamp) / total_sec
        timeWeight = round(1 / (1 + delta), 3)
        return score * timeWeight

    def get_dataset(self):
        """
        读取数据集构建`用户-电影`矩阵
        param filename : 数据集文件路径
        """
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                line = line.strip()
                line_list = line.split(',')
                user_id = line_list[0]
                item_id = line_list[1]
                score = float(line_list[2])
                timestamp = int(line_list[3])
                prefer_score = self.perfer_cal(score, timestamp)
                self.user_item.setdefault(user_id, {})
                self.user_item[user_id][item_id] = prefer_score
        print('=' * 10, '加载 %s 成功!' % self.filename, '=' * 10)

    def calc_item_sim(self):
        """
        计算电影之间的相似度
        计算方法：余弦相似度
        return:电影相似度矩阵
        """
        for user, items in self.user_item.items():
            for item in items:
                if not self.item_popular.__contains__(item):
                    self.item_popular[item] = 0
                self.item_popular[item] += 1
        self.item_count = len(self.item_popular)

        for user, items in self.user_item.items():
            for a1 in items:
                for a2 in items:
                    if a1 == a2: continue
                self.item_sim_matrix.setdefault(a1, {})
                self.item_sim_matrix[a1].setdefault(a2, 0)
                self.item_sim_matrix[a1][a2] += 1

        for a1, related_items in self.item_sim_matrix.items():
            for a2, count in related_items.items():
                if self.item_popular[a1] == 0 or self.item_popular[a2] == 0:
                    self.item_sim_matrix[a1][a2] = 0
                else:
                    self.item_sim_matrix[a1][a2] = count / sqrt(self.item_popular[a1] * self.item_popular[a2])

    def item_rec(self, user, curr_type='Action'):
        """
        针对目标用户u以及当前浏览物品c，找到与u的历史记录最相似的100部电影，产生12个推荐（与c相似的电影权重大一点）
        
        param user:目标用户u
        param curr_item:当前浏览物品c
        return: 12部推荐的电影
        """
        rank = {}
        curr_type_w = 1
        watched_items = self.user_item[user]
        for item, rating in watched_items.items():
            sorted_items = sorted(self.item_sim_matrix[item].items(), key=itemgetter(1), reverse=True)[:SIM_ITEMS]
            for related_item, w in sorted_items:
                if related_item in watched_items: continue
                if curr_type in self.movie_type.get(related_item, []):
                    curr_type_w = 3
                else:
                    curr_type_w = 1
                rank.setdefault(related_item, 0)
                rank[related_item] += w * float(rating) * curr_type_w
        res = sorted(rank.items(), key=itemgetter(1), reverse=True)[:REC_ITEMS]
        res_list = []
        for i in res:
            res_list.append(i[0])
        return res_list

    def save(self):
        with open(os.path.join(DATA_PATH, self.item_sim_name), "w") as f:
            f.write(json.dumps(self.item_sim_matrix, ensure_ascii=False, indent=4, separators=(',', ':')))
        with open(os.path.join(DATA_PATH, self.user_item_name), "w") as f:
            f.write(json.dumps(self.user_item, ensure_ascii=False, indent=4, separators=(',', ':')))


spark_master = {
    'ip': 'spark://82.156.202.134:7077'
}


def __parseFloat__(x):
    try:
        rx = float(x)
    except:
        rx = 0.0
    return rx


def __parse__(line, ifUid=False):
    l = line.split('\t')
    uid = l[0]
    label = __parseFloat__(l[1])
    features = map(lambda x: __parseFloat__(x), l[2:])
    if ifUid:
        return uid, LabeledPoint(label, features)
    else:
        return LabeledPoint(label, features)


def __intime__(args: List[str]):
    sampleHDFS_train = args
    sampleHDFS_test = args[2]
    outputHDFS = args[3]
    spark = SparkSession.builder.getOrCreate()
    conf = SparkConf().setMaster(spark_master['ip']).setAppName('{}:{}'.format(args[0], args[-1]))
    sc = spark.sparkContext

    sampleRDD = sc.textFile(sampleHDFS_train).map(__parse__)
    predictRDD = sc.textFile(sampleHDFS_test).map(lambda x: __parse__(x, True))

    model = LogisticRegressionWithLBFGS.train(sampleRDD)
    model.clearThreshold()

    labelsAndPreds = predictRDD.map(lambda p: (p[0], p[1].label, model.predict(p[1].features)))
    labelsAndPreds.map(lambda p: '\t'.join(map(str, p))).saveAsTextFile(outputHDFS + "/target/output")

    labelsAndPreds_label_1 = labelsAndPreds.filter(lambda lp: int(lp[1]) == 1)
    labelsAndPreds_label_0 = labelsAndPreds.filter(lambda lp: int(lp[1]) == 0)
    t_cnt = labelsAndPreds_label_1.count()
    f_cnt = labelsAndPreds_label_0.count()

    for thre in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
        tp = labelsAndPreds_label_1.filter(lambda lp: lp[2] > thre).count()
        tn = t_cnt - tp
        fp = labelsAndPreds_label_0.filter(lambda lp: lp[2] > thre).count()
        fn = f_cnt - fp
        print("%.1f\t%d\t%d\t%d\t%d\t%.4f\t%.4f" % (thre, tp, tn, fp, fn, float(tp) / (tp + fp), float(tp) / (t_cnt)))

    model.save(sc, outputHDFS + "/target/tmp/pythonLogisticRegressionWithLBFGSModel")
    res = LogisticRegressionModel.load(sc, outputHDFS + "/target/tmp/pythonLogisticRegressionWithLBFGSModel")
    return res


def __outtime__(args: List[str]):
    itemCF = ItemBasedCF(RATING_PATH)
    res_list = itemCF.item_rec(user=args[0], curr_type=args[1])
    return np.random.choice(res_list, 12, replace=False).tolist()


def __get_movies_id__(args: List[str]):
    try:
        return __intime__(args)
    except IndexError as e:
        print('spark is busy, switch to out time algorithm')
        return __outtime__(args)


def __get_movies__(mlist: List[str]):
    r"""
    通过推荐过来的电影id列表获取电影信息
    :param mlist: 电影id列表
    """
    mid = []
    urls = []
    names = []
    try:
        movie_list = info_dao.getMovies(mlist)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise e
    for m in movie_list:
        mid.append(m['id'])
        names.append(m['name'])
        urls.append(m['url'])
    return {'id': mid, 'name': names, 'url': urls}


def getRecomMovieList(args: List[str]):
    args[-1] = movie_tag[args[-1]]
    movies_list = __get_movies_id__(args)
    return {'result': __get_movies__(movies_list)}


if __name__ == '__main__':
    ms = getRecomMovieList(['Jocx', 1])
    print(ms)
