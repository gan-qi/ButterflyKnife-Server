# -*- coding: utf-8 -*-
from flask import request, g, session

from server import app, db
from server.models import DEP, USER, TASK, FEEDBACK

from flask_restful import Resource, Api, reqparse
from datetime import datetime

from pprint import pprint
api = Api(app)


@app.before_request
def before_request():
    """当每个请求过来时，获取其信息和token，对token进行验证，
    将用户信息设为全局
    """
    g.user_id = 1
    g.username = 'tom'


class taskOption(Resource):
    """任务的信息获取和修改
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        """获取任务信息, 以每周时间和用户id为条件查询，提供该用户的当周任务
        """
        taskInfo = TASK.query.filter_by(user_id = g.user_id).all()
        result = {
                'code': 20000,
                'data': [
                    {
                        'id': item.id,
                        'title': item.title,
                        'desc': item.desc,
                        'ctime': item.ctime.strftime('%Y-%m-%d %H:%M:%S'),
                        'wtime': item.wtime.strftime('%Y-%m-%d %H:%M:%S'),
                        'etime': item.etime.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': item.status,
                        'color': item.color,
                        'user_id': item.user_id
                        }
                    for item in taskInfo
                    ]
                }
        return result

    def post(self):
        """添加新的任务
        """
        data = request.get_json(force=True)
        newTask = TASK(title=data.get('title'), desc=data.get('desc'),
                ctime=datetime.now(),
                wtime=datetime.now(),
                etime=datetime.now(),
                status = 0,
                color='black',
                user_id=g.user_id
                )
        db.session.add(newTask)
        db.session.commit()
        targetTaskInfo = TASK.query.filter_by(title=data.get('title'),
                desc=data.get('desc'), status=0, color='black',
                user_id=g.user_id).first()
        return {
                'code': 20000,
                'data': {
                    'id': targetTaskInfo.id,
                    'title': targetTaskInfo.title,
                    'desc': targetTaskInfo.desc,
                    'ctime': targetTaskInfo.ctime.strftime('%Y-%m-%d %H:%M:%S'),
                    'wtime': targetTaskInfo.wtime.strftime('%Y-%m-%d %H:%M:%S'),
                    'etime': targetTaskInfo.etime.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': targetTaskInfo.status,
                    'color': targetTaskInfo.color,
                    'user_id': targetTaskInfo.user_id
                    }
                }


class taskIdOption(Resource):
    """任务的删除和状态变更"""

    def option(self, taskid):
        return {
                'code': 20000
                }

    def delete(self, taskid):
        """删除任务
        """
        deleteTask = TASK.query.filter_by(id=taskid).first()
        db.session.delete(deleteTask)
        db.session.commit()
        return {
                'code': 20000
                }

    def post(self, taskid):
        """更新任务状态，修改信息
        """
        data = request.get_json(force=True)
        newTask = TASK.query.filter_by(id=taskid).first()
        newTask.title = data.get('title')
        newTask.desc = data.get('desc')
        newTask.color = data.get('color')
        newTask.status = data.get('status')
        # 正在进行和完成的时间，当时间存在则更改相应的状态
        if newTask.status != data.get('status'):
            if data.get('status') == 1:
                newTask.wtime = datetime.now()
            if data.get('status') == 2:
                newTask.etime = datetime.now()
        db.session.commit()
        return {
                'code': 20000
                }


class feedBack(Resource):
    """反馈"""

    def option(self):
        return {
                'code': 20000
                }

    def post(self):
        data = request.get_json(force=True)
        newFeedBack = FEEDBACK(content=data.get('content'))
        db.session.add(newFeedBack)
        db.session.commit()
        return {
                'code': 20000
                }


class Login(Resource):
    """用户登陆
    """

    def post(self):
        data = request.get_json(force=True)
        # 检查用户名密码是否正确
        if not data.get('username'):
            return {
                    'code': 40001,
                    'message': '登陆失败'
                    }
        tokens = {
                'admin': {
                    'token': 'admin-token'
                    },
                'user': {
                    'token': 'editor-token'
                    }
                }
        print(tokens.get(data.get('username')))
        return {
                'code': 20000,
                'data': {
                    'token': tokens.get(data.get('username'))
                    }
                }


class userInfo(Resource):
    """获取用户信息
    """

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', type=str)

    def get(self):
        data = self.parser.parse_args()
        token = json.loads(data.get('token')).get('token')
        users = {
                'editor-token': {
                    'roles': ['editor'],
                    'introduction': '用户甲',
                    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                    'name': '普通用户'
                    },
                'admin-token': {
                    'roles': ['admin'],
                    'introduction': '超级管理员',
                    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
                    'name': '超级管理员'
                    }
                }
        return {
                'code': 20000,
                'data': users.get(token)
                }


class Logout(Resource):
    """登出
    input: b''
    ouput: {
        'code': 20000,
        'data': 'success'
    }
    """
    def post(self):
        return {
                'code': 20000,
                'data': 'success'
                }

api.add_resource(taskOption, '/task')
api.add_resource(taskIdOption, '/task/<taskid>')
api.add_resource(feedBack, '/feedback')
api.add_resource(Login, '/user/login')
api.add_resource(userInfo, '/user/info')
api.add_resource(Logout, '/user/logout')
