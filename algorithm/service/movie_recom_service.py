#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/5 13:26
@Author : Jocx-H
@File   : movie_recom_service.py
@Desc   :  PyCharm
'''

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from time import *
from typing import List

import json
import numpy
import os
import random
import sys
import traceback


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
    spark = SparkSession.builder.getOrCreate()
    conf = SparkConf().setMaster(spark_master['ip']).setAppName('{}:{}'.format(args[0], args[-1]))
    sc = spark.sparkContext
    sampleHDFS_train = args
    sampleHDFS_test = sys.argv[2]
    outputHDFS = sys.argv[3]

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
        print("%.1f\t%d\t%d\t%d\t%d\t%.4f\t%.4f"%(thre, tp, tn, fp, fn, float(tp)/(tp+fp), float(tp)/(t_cnt)))

    model.save(sc, outputHDFS + "/target/tmp/pythonLogisticRegressionWithLBFGSModel")
    res = LogisticRegressionModel.load(sc, outputHDFS + "/target/tmp/pythonLogisticRegressionWithLBFGSModel")
    return res


def __outtime__(args: List[str]):
    return [{'id': 'lalal', 'name': 'ddd', 'url': 'sdfsdf'}]


def __get_movies__(args: List[str]):
    try:
        return __intime__(args)
    except IndexError as e:
        print('spark is busy, switch to out time algorithm')
        return __outtime__(args)
    except Exception as e:
        raise e


def getRecomMovieList(args: List[str]):
    movies_list = __get_movies__(args)
    mid, urls, names = [], [], []
    for m in movies_list:
        mid.append(m['id'])
        names.append(m['name'])
        urls.append(m['url'])
    return {'result': {'id': mid, 'name': names, 'url': urls}}


if __name__ == '__main__':
    ms = getRecomMovieList(['Jocx', '1', '4', '1256677221'])
    print(ms)