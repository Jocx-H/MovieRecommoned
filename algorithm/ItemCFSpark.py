#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File   :   ItemCF.py
@Time   :   2022/06/23 15:17:41
@Author :   ferry-hhh
@Desc   :   基于物品的推荐，放在详情页
'''

from math import sqrt
from operator import itemgetter
import json
import os

RATING_PATH = os.getcwd() + "\data\ratings.csv"
DATA_PATH = os.getcwd() + "\data"

# 在首页/详情页推荐20部电影
REC_ITEMS = 12
# 与目标电影相似的100部其他电影
SIM_ITEMS = 100
# 当前时间戳（最大时间戳）
MAX_TIMESTAMP = 1537945149

def perfer_cal(score,timestamp):
    """
    综合用户评分、时间戳得到一个综合评分
    
    param line:数据库中的一行数据
    return:综合评分
    """
    total_sec = 24 * 60 * 60 * 365 * 10
    delta = (MAX_TIMESTAMP - timestamp) / total_sec
    # delta 越小，得分越高，最高分为1
    timeWeight = round(1 / (1 + delta), 3)
    return score * timeWeight


class ItemBasedCF():
    def __init__(self, filename):
        """
        初始化参数
        """
        # 用户-电影矩阵
        # {u1:{i1:9,i2:7,i3:8},
        #  u2:{i2:9,i4:8,i5:10}}
        self.user_item = {}
        # 电影相似度矩阵
        # {i1:{i1:0,i2:0.8,i3:0.2},
        #  i2:{i1:0.8,i2:0,i3:0.1},
        #  i3:{i1:0.2,i2:0.1,i3:0}}
        self.item_sim_matrix = {}
        # 电影热度列表，值是喜欢该电影的人数
        # {i1:4,
        #  i2:5,
        #  i3:2}
        self.item_popular = {}
        # 电影类型
        # {i1:['Action','War'],
        #  i2:['War','Comedy']}
        self.movie_type = {}
        self.item_count = 0
        self.filename = filename
        self.user_item_name = "movie_user_item.json"
        self.item_sim_name = "movie_item_sim.json"
        self.movie_type_name = "sorted.json"
        with open(os.path.join(DATA_PATH, self.movie_type_name), "r") as f3:
            self.movie_type = json.load(f3)
        # 首先检查是否已经预处理完成了用户-物品矩阵与用户相似度矩阵
        try:
            with open(os.path.join(DATA_PATH, self.user_item_name), "r") as f1:
                self.user_item = json.load(f1)
            with open(os.path.join(DATA_PATH, self.item_sim_name), "r") as f2:
                self.item_sim_matrix = json.load(f2)
        except FileNotFoundError:
            self.get_dataset()
            self.calc_item_sim()
            self.save()

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
                prefer_score = perfer_cal(score, timestamp)
                self.user_item.setdefault(user_id, {})
                self.user_item[user_id][item_id] = prefer_score
        print('='*10, '加载 %s 成功!' % self.filename, '='*10)

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
        print('='*10, '电影热度列表构建完毕', '='*10)
        self.item_count = len(self.item_popular)

        # 共现矩阵，C[i][j]代表的含义是同时喜欢物品i和物品j的用户数量
        # {i1:{i1:0,i2:1,i3:3},
        #  i2:{i1:1,i2:0,i3:2},
        #  i3:{i1:3,i2:2,i3:0}}
        for user, items in self.user_item.items():
            for a1 in items:
                for a2 in items:
                    if a1 == a2:continue
                self.item_sim_matrix.setdefault(a1, {})
                self.item_sim_matrix[a1].setdefault(a2, 0)
                self.item_sim_matrix[a1][a2] += 1
        print('='*10, '电影共现矩阵构建完毕', '='*10)

        # 计算电影之间的相似性
        for a1, related_items in self.item_sim_matrix.items():
            for a2, count in related_items.items():
                if self.item_popular[a1] == 0 or self.item_popular[a2] == 0:
                    self.item_sim_matrix[a1][a2] = 0
                else:
                    self.item_sim_matrix[a1][a2] = count / sqrt(self.item_popular[a1]*self.item_popular[a2])
        print('='*10, '电影相似度矩阵构建完毕', '='*10)

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
            # 与历史记录电影最相似的100部电影
            sorted_items = sorted(self.item_sim_matrix[item].items(), key=itemgetter(1), reverse=True)[:SIM_ITEMS]
            # related_item是相关电影，w是当前电影与相关电影的相似度，rating是目标用户对当前电影的评分
            for related_item, w in sorted_items:
                if related_item in watched_items:continue
                if curr_type in self.movie_type.get(related_item, []):
                    curr_type_w = 3
                else:
                    curr_type_w = 1
                rank.setdefault(related_item, 0)
                rank[related_item] += w * float(rating) * curr_type_w
        res = sorted(rank.items(), key=itemgetter(1), reverse=True)[:REC_ITEMS]

        print('推荐12部电影：', res)
        return res

    def save(self):
        with open(os.path.join(DATA_PATH, self.item_sim_name), "w") as f:
            f.write(json.dumps(self.item_sim_matrix, ensure_ascii=False, indent=4, separators=(',', ':')))
        with open(os.path.join(DATA_PATH, self.user_item_name), "w") as f:
            f.write(json.dumps(self.user_item, ensure_ascii=False, indent=4, separators=(',', ':')))
        print('='*10, '用户-物品矩阵与物品相似度矩阵保存成功', '='*10)

if __name__ == "__main__":
    userCF = ItemBasedCF(RATING_PATH)
    userCF.item_rec("Jocx", curr_type='Comedy')
    userCF.item_rec("Jocx", curr_type='Sci-Fi')
    userCF.item_rec("Jocx", curr_type='Action')
    # userCF.item_rec("15")
    # userCF.item_rec("200")
