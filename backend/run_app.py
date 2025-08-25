#!/usr/bin/env python3
"""
Simple script to run the Flask app
"""
from flaskr import create_app
from models import setup_db, Question, Category, db

def init_db():
    """Initialize the database with sample data"""
    app = create_app()
    with app.app_context():
        setup_db(app)
        
        # Check if categories already exist
        if Category.query.count() == 0:
            # Add categories
            categories = [
                "Science",
                "Art", 
                "Geography",
                "History",
                "Entertainment",
                "Sports"
            ]
            
            for category_name in categories:
                category = Category(type=category_name)
                db.session.add(category)
                db.session.commit()
                print(f"Added category: {category_name}")
        
        # Check if questions already exist
        if Question.query.count() == 0:
            # Add some sample questions
            questions = [
                {
                    "question": "What is the largest planet in our solar system?",
                    "answer": "Jupiter",
                    "category": "1",
                    "difficulty": 2
                },
                {
                    "question": "Who painted the Mona Lisa?",
                    "answer": "Leonardo da Vinci",
                    "category": "2",
                    "difficulty": 1
                },
                {
                    "question": "What is the capital of France?",
                    "answer": "Paris",
                    "category": "3",
                    "difficulty": 1
                },
                {
                    "question": "In which year did World War II end?",
                    "answer": "1945",
                    "category": "4",
                    "difficulty": 2
                },
                {
                    "question": "Who directed the movie Titanic?",
                    "answer": "James Cameron",
                    "category": "5",
                    "difficulty": 2
                },
                {
                    "question": "Which country won the FIFA World Cup in 2018?",
                    "answer": "France",
                    "category": "6",
                    "difficulty": 2
                }
            ]
            
            for q_data in questions:
                question = Question(
                    question=q_data["question"],
                    answer=q_data["answer"],
                    category=q_data["category"],
                    difficulty=q_data["difficulty"]
                )
                question.insert()
                print(f"Added question: {q_data['question']}")
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)