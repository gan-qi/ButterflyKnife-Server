# -*- coding: utf-8 -*-
from flask import request

from server import app, db
from server.models import ARCHIVE_INDEX, ARCHIVE, ARTICLE, TOPIC

from flask_restful import Resource, Api, reqparse

from server.getArticleContent import getAC

api = Api(app)


class getArticleList(Resource):
    """获取首页的文章列表。
    """

    def option(self):
        return {
                'code': 20000
                }

    def get(self):
        articles = ARTICLE.query.filter_by(\
                active=1).order_by( ARTICLE.id.desc() ).limit(20).all()
        articles = [ dict( id=item.id, title=item.title, \
                    time=item.time, archive=item.archive, \
                    intro=item.intro) for item in articles ]
        return {
                'code': 20000,
                'data': articles
                }

    def post(self):
        data = request.get_json(force=True)
        count = data.get('count')
        lists = ARTICLE.query.filter_by(\
                active=1).order_by( ARTICLE.id.desc()\
                        ).offset(count).limit(20).all()
        articles = [ dict( id=item.id, title=item.title, \
                    time=item.time, archive=item.archive, \
                    intro=item.intro) for item in lists ]
        return {
                'code': 20000,
                'data': articles
                }


class getArticleContent(Resource):
    """获取具体文章的内容
    """

    def get(self, article_id):
        article = ARTICLE.query.filter_by( id = article_id ).first()
        return {
                'code': 20000,
                'data': {
                    'title': article.title,
                    'time': article.time,
                    'archive': article.archive,
                    'content': getAC(article_id)
                    }
                }


api.add_resource(getArticleList, '/getarticlelist')
api.add_resource(getArticleContent, '/getarticlecontent/<int:article_id>')
