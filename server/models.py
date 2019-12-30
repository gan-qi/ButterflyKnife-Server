# -*- coding: utf-8 -*-
from server import db

"""
表： 分类索引 分类 文章 专题

分类索引： ID 分类名
archive_index: id ai_name

分类：ID 分类名 分类索引
archive: id a_name ai_id

文章: ID 名字 时间 分类
article: id title time archive_id

"""
# 分类索引
class ARCHIVE_INDEX(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ai_name = db.Column(db.String(10), nullable=False)

# 分类
class ARCHIVE(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_name = db.Column(db.String(20), nullable=False)
    ai_id = db.Column(db.Integer, nullable=False)

# 文章
class ARTICLE(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.String(20), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    active = db.Column(db.Integer, nullable=False)
