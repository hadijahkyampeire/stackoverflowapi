from datetime import datetime
from flask import Flask, jsonify, request, make_response
from api.models import Questions, User
from api.auth.decorator import token_required
from api.database import Database
from api import app


db = Database('postgresql://postgres:0000@localhost/stackoverflow')

@app.route('/api/v1/questions', methods=['POST'])
@token_required
def post_question(current_user):
    """This routes add questions"""
    data = request.get_json()
    title = data['title']
    description = data['description']
    owner = current_user.user_id
    date = datetime.now()
    if not title:
        return jsonify({"msg": "Title field is empty"}), 400
    if db.get_by_argument('questions','title', title):
        return jsonify({'message': 'Question already asked'}), 409
    db.insert_question_data(owner, title, description, date)
    return jsonify({'message':'Question created successfully'}), 201

@app.route('/api/v1/questions', methods=['GET'])
@token_required
def get_all_questions(current_user):
    """This route returns all the questions"""
    questions = db.fetch_all()
    if questions == []:
        return jsonify(
                    {"message": " There are no questions asked"
                     }), 404
    return jsonify(questions), 200

@app.route('/api/v1/question/<int:question_id>', methods=['GET'])
@token_required
def get_question_by_id(current_user, question_id):
    """This returns a question by id"""
    question = db.get_by_argument('questions', 'question_id', question_id)
    if question:
        response = {'question_id': question[0], 'title':question[2], 'description':question[3], 'user_id':question[1]}
        answers = db.query_all_where_id("answers", "question_id", question_id)
        # answer_response = {'answer_id': answers[0], 'question_id':answers[1], 
        #     'reply': answers[2], 'user':answers[3], 'preffered':answers[4]}
        return jsonify({'question':response, 'answers': answers}), 200
    return jsonify({'message':'No question by that id'}), 404


@app.route('/api/v1/question/<int:question_id>', methods=['DELETE'])
@token_required
def delete_question_by_id(current_user, question_id):
    """This returns a question by id"""
    user_id = current_user.user_id
    question = db.get_by_argument('questions', 'user_id', user_id)
    if question:
        if user_id in question:
            db.delete_question(question_id)
            return jsonify({'message':'Question deleted successfully with all its answers'}), 200
        return jsonify({'Warning':'You have no rights to delete this question'})
    return jsonify({'message':'No question by that id'}), 404


