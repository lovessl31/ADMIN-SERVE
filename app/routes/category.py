from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
import sqlite3
from app.database import db_manager as DB
from app.utils import get_t_com, is_list, connect_to_db, connect_to_dbs



cate_api = Namespace('Category', description='카테고리 API', path='/with')


@cate_api.route('/cate')
class category(Resource):
    @jwt_required()
    def get(self):
        """
            전체 카테고리 조회

            get 요청으로 전체 카테고리를 조회합니다.
        """
        # 토큰에 있는 유저정보 가져오기
        data = get_jwt_identity()
        print("category get data::",data)
        if data:
            # 회사 경로
            if not get_t_com(data):
                return jsonify({'idxError':'회사정보가 존재하지않습니다.'},401)
            else:
                paths = get_t_com(data)[0]
            # 리스트 형식이라면 모든 서브db를 순회
            if is_list(paths):
                result = connect_to_dbs(paths, "category")
                return jsonify(result, 200)
            # 리스트가 아니라면 최고관리자가 아니기때문에
            else:
                conn = sqlite3.connect(paths)
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM category''')
                categories = []
                for row in cursor.fetchall():
                    cate_val = list(row)
                    cursor.execute('''SELECT tag_name FROM c_tag WHERE cate_idx = ?''', (cate_val[0],))
                    tag = cursor.fetchall()
                    # null 값 0으로
                    if cate_val[1] is None:
                        cate_val[1] = 0
                    categories.append({'cateNo': cate_val[0],
                                       'subCateNo': cate_val[1],
                                       'categoryName': cate_val[2],
                                       'categoryType': cate_val[3],
                                       'role': cate_val[4],
                                       'visibility': cate_val[5],
                                       'likeSet': cate_val[6],
                                       'tag': tag
                                       })
                return jsonify(categories, 200)
        else:
            return 'Your browser sent a request that this server could not understand.', 400

@cate_api.route('/cate/first/{CateSecondId}/second')
class category(Resource):
    def get(self):
        """
        2차 카테고리 조회

        GET 요청으로 2차 카테고리를 조회합니다.
        """


@cate_api.route('/cate/second')
class category(Resource):
    @cate_api.doc(description="2차 카테고리 등록",
                  params={'cate_name':'카테고리명',
                          'cate_type': 'P/L(앨범,리스트)',
                          "role": "Number",
                          'cate_vis': 'Y/N',
                          'LikeSet':'Y/N',
                          'tag': '["value1", "value2", "value3"]'
                          },
                  responses={200: 'First add category'})
    def post(self):
        """
            2차 카테고리 생성

            POST 요청으로 카테고리를 생성합니다.
        """

        return {"카테고리": "post success!!"}


@cate_api.route('/cate/first')
class category(Resource):
    @jwt_required()
    @cate_api.doc(description="카테고리 등록",
                  params={'cate_name':'카테고리명',
                          'cate_type': 'P/L(앨범,리스트)',
                          "role": "Number",
                          'cate_vis': 'Y/N',
                          'LikeSet': 'Y/N',
                          'tag': '["value1", "value2", "value3"]'
                          },
                  responses={200: 'First add category'})
    def post(self):
        """
            카테고리 생성

            POST 요청으로 카테고리를 생성합니다.
        """
        # 토큰에 있는 정보 가져오기
        t_data = get_jwt_identity()
        data = request.json

        if t_data and data:
            try:
                # 회사 경로
                row = get_t_com(t_data)
                path = row[0]
                conn = sqlite3.connect(path)
                p_idx = 0
                c_name = data.get('cate_name')
                c_type = data.get('cate_type')
                role = data.get('role')
                c_vis = data.get('cate_vis')
                l_set = data.get('LikeSet')
                tagList = data.get('tag', [])
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO category 
                                             (p_cate_idx, cate_name, cate_type, role, cate_vis, LikeSet)
                                             VALUES(?,?,?,?,?,?)''', (p_idx, c_name, c_type, role, c_vis, l_set))
                c_idx = cursor.lastrowid
                # 말머리가 존재하면 하나씩 데이터 삽입.
                if tagList:
                    for tag in tagList:
                        cursor.execute('''INSERT INTO c_tag (cate_idx, tag_name) VALUES(?,?)''', (c_idx, tag))
                conn.commit()
                conn.close()
            except Exception as e:
                # 오류 처리
                return jsonify({'Error': str(e)}, 500)
            finally:
                conn.close()
            return jsonify({"success":"suc"},200)

        else:
            return jsonify({'DataError':'Your browser sent a request that this server could not understand.'}), 400


@cate_api.route('/cate/{cateIdx}')
class category(Resource):
    def put(self):
        """
            카테고리 수정

            POST 요청으로 1,2차 카테고리를 수정합니다.
        """

        return {"카테고리": "delete success!!"}

    def get(self):
        """
            카테고리 상세 조회

            get 요청으로 카테고리를 조회합니다.
        """

        return {"카테고리": "get success!!"}

    def delete(self):
        """
            카테고리 삭제

            delete 요청으로 카테고리를 삭제합니다.
        """

        return {"카테고리": "delete success!!"}