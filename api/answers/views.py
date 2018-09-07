from flask import Flask, jsonify, request, make_response
from api.models import Questions, User
from api.auth.decorator import token_required
from api.database import Database
from api import app

db = Database()

@app.route('/api/v1/question/<int:question_id>/answers', methods=['POST'])
@token_required
def post_answer(current_user, question_id):
    """This routes add answers to questions"""
    data = request.get_json()
    reply = data['reply']
    owner = current_user.user_id
    if not reply:
            return jsonify({"msg": "Reply field is empty"}), 400
    if db.get_by_argument('answers','reply', reply):
        return jsonify({'message': 'Answer already given'}), 409
    db.insert_answer_data(question_id,reply, owner)
    return jsonify({'message':'Answer added to the question successfully'}), 201

@app.route('/api/v1/question/<int:question_id>/answers/<int:answer_id>/accept', methods=['PUT'])
@token_required
def accept_answer(current_user, question_id, answer_id):
    """This routes add answers to questions"""
    owner = current_user.user_id
    question = db.get_by_argument('questions', 'question_id', question_id)
    if question:
        value = "True"
        db.update_answer_record("answers", "preffered", value, "answer_id", answer_id)
        return jsonify({'message':'Answer update successfully'}), 201
    return jsonify({'message':'No question by that id'}), 404

@app.route('/api/v1/question/<int:question_id>/answers/<int:answer_id>/update', methods=['PUT'])
@token_required
def update_answer(current_user, question_id, answer_id):
    """This routes add answers to questions"""
    data = request.get_json()
    reply = data['reply']
    owner = current_user.user_id
    if not reply:
        return jsonify({"msg": "Reply field is empty"}), 400
    if db.get_by_argument('answers','reply', reply):
        return jsonify({'message': 'Answer already given'}), 409
    question = db.get_by_argument('questions', 'question_id', question_id)
    if question:
        db.update_answer_record("answers", "reply", reply, "answer_id", answer_id)
        return jsonify({'message':'Answer Edited to the question successfully'}), 201
    return jsonify({'message':'No question by that id'}), 404