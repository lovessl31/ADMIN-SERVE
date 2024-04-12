from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify
import sqlite3
from app.database import db_manager as DB


board_api = Namespace('Board', description='게시판 API', path='/with/board')

@board_api.route('/post/{postId}')
class posts(Resource):
    def delete(self):
        """
                게시판 글 삭제

                DELETE 요청으로 게시글을 삭제합니다.
                """
        return {"delete": "success!!"}

    def put(self):
        """
                게시판 글 수정

                PUT 요청으로 게시글을 수정합니다.
                """
        return {"PUT": "success!!"}

    def get(self):
        """
                게시판 글 상세

                GET 요청으로 게시글을 조회합니다.
                """
        return {"GET": "success!!"}


@board_api.route('/{boardName}')
class board(Resource):
    def get(self):
        """
                게시판 정보조회

                GET 요청으로 게시판을 조회합니다.
                """
        return {"GET": "success!!"}

    def post(self):
        """
                게시판 작성

                POST 요청으로 게시판을 작성합니다.
                """
        return {"GET": "success!!"}


@board_api.route('/{boardName}/posts')  # 리스트
class post_list(Resource):
    def get(self):
        """
                게시글 리스트 조회

                GET 요청으로 게시글 목록을 조회합니다.
                """
        return {"GET": "success!!"}