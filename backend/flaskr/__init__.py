import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS #, cross_origin
import random

from backend.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    """

    Serve React frontend - must be first to avoid conflicts with API routes
    """
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # Don't serve React for API routes
        if path.startswith(('categories', 'questions', 'quizzes')):
            abort(404)
        if os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        else:
            return app.send_static_file('index.html')
    
    """

    Create an endpoint to handle GET requests for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def all_categories():
        categories = Category.query.order_by(Category.id).all()
        categories_result = {}
        for cat in categories:
            categories_result[cat.id] = cat.type

        return jsonify({
            "success": True,
            "categories": categories_result
        })

    """

    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def paginate_questions(request, selection):
        """
        HELPER FUNCTION!    
        """
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE 
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        
        return current_questions
    
    @app.route('/questions')
    def get_questions():

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if not current_questions:
            abort(404)
        
        categories = Category.query.order_by(Category.id).all()
        categories_result = {}
        for cat in categories:
            categories_result[cat.id] = cat.type

        if len(current_questions) == 0:
            abort(404)

        #return a list of questions, number of total questions, current category, categories.

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': None,
            'categories': categories_result
        })
    
    """

    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter(Question.id==question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
            'success':True,
            'deleted':question_id,
            'questions':current_questions,
            'total_questions': len(selection)
        })

    """

    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
            
    """

    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    #POST to search and create
    
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()
        search_term = body.get('searchTerm')
        
        # SEARCHING
        
        if search_term:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(questions),
                "current_category": None
            })
        
        # CREATING
        
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        new_difficulty = body.get('difficulty')
        
        if not all([new_question, new_answer, new_category, new_difficulty]):
            abort(400)
        
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=int(new_difficulty))

        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)


        return jsonify({
            'success' : True,
            'created' : question.id,
            'questions' : current_questions,
            'total_questions' : len(selection)
        })

    """

    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        category = Category.query.get_or_404(category_id)

        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": category_id
        })

    """

    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def create_quizzes():
        body = request.get_json(force=True, silent=True) or {}
        if "previous_questions" not in body:
            abort(400)
        #previous_questions = body.get("previous_questions", [])
        previous_questions = body["previous_questions"]
        
        quiz_category = body.get("quiz_category")
        if isinstance(quiz_category, dict):
            category_id = int(quiz_category.get("id", 0))
            
        elif quiz_category in (None, "", "0"):
            category_id = 0
        else:
            category_id = int(quiz_category)

        query = Question.query.filter(~Question.id.in_(previous_questions))
        if category_id:
            query = query.filter(Question.category == str(category_id))

        questions = query.all()
        next_question = random.choice(questions).format() if questions else None

        return jsonify({
            "success": True, 
            "question": next_question
        })

    
    """

    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify ({
            'success':False,
            'error':404,
            'message':'Page not found'
            }), 404 

    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify ({
            'success':False,
            'error':400,
            'message':'Bad Request, add more info :('
            }), 400 


    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify ({
            'success':False,
            'error':422,
            'message':'Unprocessable'
            }), 422 
    
    
    @app.errorhandler(405)
    def not_found(error):
        return jsonify ({
            'success':False,
            'error':405,
            'message':'Method not allowed'
            }), 405 
    
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify ({
            "success":False,
            "error":500,
            "message":'Internal Server Error'
        }), 500
    
    
    return app

# Create the app instance for Gunicorn
app = create_app()
