from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify
import sqlite3
from app.database import db_manager as DB


comment_api = Namespace('Comment', description='댓글 API', path='/with/cm')


# 댓글 삭제
@comment_api.route('/{cmIdx}')
class comment(Resource):
    def delete(self):
        """
        유저 댓글 삭제

        DELETE 요청으로 댓글을 삭제합니다.
        """

    def post(self):
        """
        유저 답글 등록

        post 요청으로 답글을 추가합니다.
        """