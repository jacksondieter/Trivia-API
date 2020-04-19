import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def format_categories(selection):
    categories_list = [category.format() for category in selection]
    categories_object = {category['id']:category['type'].lower() for category in categories_list}
    return categories_object

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        categories = format_categories(selection)

        if len(categories.keys()) == 0:
            abort(404)
        return jsonify({'success': True,'categories': categories})

    @app.route('/questions')
    def retrieve_questions():

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        selection = Category.query.order_by(Category.id).all()
        categories = format_categories(selection)
        current_category = categories[current_questions[0]['category']]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'current_category':current_category,
            'categories':categories

        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True
            })

        except:
            abort(422)


    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        search = body.get('searchTerm', None)
        if search != None:
            questions = Question.query.filter(Question.question.ilike('%'+search+'%')).all()
            questions = [question.format() for question in questions]
            selection = Category.query.order_by(Category.id).all()
            categories = format_categories(selection)
            current_category = categories[questions[0]['category']]
            if len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category':current_category
            })
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            try:
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'question_id': question.id
                })

            except:
                abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def list_questions(category_id):

        selection = Question.query.filter(Question.category == category_id).all()
        questions = [question.format() for question in selection]
        category = Category.query.filter_by(id=category_id).one_or_none()
        current_category = category.format()['type']

        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_question': len(questions),
            'current_category': current_category
        })

    @app.route('/quizzes', methods=['POST'])
    def get_question_for_quiz():
        body = request.get_json()
        if 'quiz_category' in body:
            previous_questions =  body.get('previous_questions',[])
            category =  body.get('quiz_category')
            if category['id']==0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == category['id']).all()
            rest_questions = [question.format() for question in questions]
            rest_questions = [question for question in rest_questions if question['id'] not in previous_questions ]

            if len(rest_questions) > 0:
                question = rest_questions[random.randint(0,len(rest_questions)-1)]
                print(question)
                return jsonify({
                    'success': True,
                    'question':question
                    })
            else:
                return jsonify({
                    'success': True,
                    'question':None
                    })
        abort(404)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app