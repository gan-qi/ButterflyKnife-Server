#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from server import db

'''
表： 部门(department)  角色(role)  用户(user)  任务(task)

部门：       序号     名称
DEPARTMENT： id       name

用户：       序号    名称     角色     密码
USER：       id      name     role     password

任务：       序号    名称   描述   创建时间   工作时间    完成时间     状态     色彩
TASK：       id      title   desc    ctime      wtime       etime      status    color

'''

# 部门
class DEP(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

# 用户
class USER(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.Integer, nullable=False, default=2)
    password = db.Column(db.String(256), nullable=False)
    dep_id = db.Column(db.Integer, db.ForeignKey('DEP.id'))
    deps = db.relationship('DEP', backref='user')

# 任务
class TASK(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    desc = db.Column(db.Text)
    ctime = db.Column(db.DateTime, nullable=False)
    wtime = db.Column(db.DateTime, nullable=False)
    etime = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    color = db.Column(db.String(10), default='#FFF')
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    tasks = db.relationship('USER', backref='task')

# 反馈
class FEEDBACK(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
