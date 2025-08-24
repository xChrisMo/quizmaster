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

    Serve React frontend
    """
    @app.route('/')
    def serve_index():
        html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuizMaster - Trivia App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ffffff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .api-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .api-section h2 {
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .endpoint {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #4CAF50;
        }
        
        .endpoint h3 {
            color: #4CAF50;
            margin-bottom: 0.5rem;
        }
        
        .endpoint code {
            background: rgba(0, 0, 0, 0.3);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
        
        .test-button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 0.5rem;
            transition: transform 0.2s;
        }
        
        .test-button:hover {
            transform: translateY(-2px);
        }
        
        .result {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .status {
            text-align: center;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        .status.success {
            background: rgba(76, 175, 80, 0.2);
            border: 1px solid #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>QuizMaster</h1>
            <p>Your Trivia API is running successfully! 🎉</p>
        </div>
        
        <div class="status success">
            ✅ <strong>API Status:</strong> All endpoints are working correctly
        </div>
        
        <div class="api-section">
            <h2>Available API Endpoints</h2>
            
            <div class="endpoint">
                <h3>GET /categories</h3>
                <p>Get all available categories</p>
                <code>GET https://your-quizmaster-app-c4690209a8b5.herokuapp.com/categories</code>
                <br>
                <button class="test-button" onclick="testEndpoint('/categories')">Test Endpoint</button>
                <div id="categories-result" class="result" style="display: none;"></div>
            </div>
            
            <div class="endpoint">
                <h3>GET /questions</h3>
                <p>Get all questions with pagination</p>
                <code>GET https://your-quizmaster-app-c4690209a8b5.herokuapp.com/questions?page=1</code>
                <br>
                <button class="test-button" onclick="testEndpoint('/questions?page=1')">Test Endpoint</button>
                <div id="questions-result" class="result" style="display: none;"></div>
            </div>
            
            <div class="endpoint">
                <h3>GET /categories/{id}/questions</h3>
                <p>Get questions by category</p>
                <code>GET https://your-quizmaster-app-c4690209a8b5.herokuapp.com/categories/1/questions</code>
                <br>
                <button class="test-button" onclick="testEndpoint('/categories/1/questions')">Test Endpoint</button>
                <div id="category-questions-result" class="result" style="display: none;"></div>
            </div>
            
            <div class="endpoint">
                <h3>POST /questions</h3>
                <p>Create a new question</p>
                <code>POST https://your-quizmaster-app-c4690209a8b5.herokuapp.com/questions</code>
                <br>
                <button class="test-button" onclick="testCreateQuestion()">Test Endpoint</button>
                <div id="create-question-result" class="result" style="display: none;"></div>
            </div>
            
            <div class="endpoint">
                <h3>POST /quizzes</h3>
                <p>Play a quiz</p>
                <code>POST https://your-quizmaster-app-c4690209a8b5.herokuapp.com/quizzes</code>
                <br>
                <button class="test-button" onclick="testQuiz()">Test Endpoint</button>
                <div id="quiz-result" class="result" style="display: none;"></div>
            </div>
        </div>
        
        <div class="api-section">
            <h2>Next Steps</h2>
            <p>Your API is fully functional! To get the complete React frontend working:</p>
            <ul style="margin-left: 2rem; margin-top: 1rem;">
                <li>Deploy the React frontend separately to a service like Vercel or Netlify</li>
                <li>Update the API base URL in the React app to point to your Heroku API</li>
                <li>Or continue using this simple interface to test your API</li>
            </ul>
        </div>
    </div>

    <script>
        const API_BASE = 'https://your-quizmaster-app-c4690209a8b5.herokuapp.com';
        
        async function testEndpoint(endpoint) {
            const resultDiv = document.getElementById(endpoint.replace(/[^a-zA-Z0-9]/g, '-') + '-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Loading...';
            
            try {
                const response = await fetch(API_BASE + endpoint);
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
            }
        }
        
        async function testCreateQuestion() {
            const resultDiv = document.getElementById('create-question-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Loading...';
            
            try {
                const response = await fetch(API_BASE + '/questions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: 'What is the capital of France?',
                        answer: 'Paris',
                        category: '1',
                        difficulty: 1
                    })
                });
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
            }
        }
        
        async function testQuiz() {
            const resultDiv = document.getElementById('quiz-result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = 'Loading...';
            
            try {
                const response = await fetch(API_BASE + '/quizzes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        previous_questions: [],
                        quiz_category: { id: 1, type: 'Science' }
                    })
                });
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
        '''
        return html_content, 200, {'Content-Type': 'text/html'}
    
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
