#!/usr/bin/env python3
"""
Script to add sample data to the database
"""
from backend.models import setup_db, Question, Category
from backend.flaskr import create_app

def add_sample_data():
    app = create_app()
    with app.app_context():
        setup_db(app)
        
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
            category.insert()
            print(f"Added category: {category_name}")
        
        # Add some sample questions
        questions = [
            {
                "question": "What is the largest planet in our solar system?",
                "answer": "Jupiter",
                "category": "Science",
                "difficulty": 2
            },
            {
                "question": "Who painted the Mona Lisa?",
                "answer": "Leonardo da Vinci",
                "category": "Art",
                "difficulty": 1
            },
            {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "category": "Geography",
                "difficulty": 1
            },
            {
                "question": "In which year did World War II end?",
                "answer": "1945",
                "category": "History",
                "difficulty": 2
            },
            {
                "question": "Who directed the movie Titanic?",
                "answer": "James Cameron",
                "category": "Entertainment",
                "difficulty": 2
            },
            {
                "question": "Which country won the FIFA World Cup in 2018?",
                "answer": "France",
                "category": "Sports",
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
        
        print("Sample data added successfully!")

if __name__ == "__main__":
    add_sample_data()
