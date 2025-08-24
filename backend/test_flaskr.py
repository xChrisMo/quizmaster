import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgresql://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
            category = Category(type="Science")
            self.db.session.add(category)
            self.db.session.commit()

            question = Question(question="What is H2O commonly known as?",
                         answer="Water",
                         category=str(category.id),
                         difficulty=1)
            self.db.session.add(question)
            self.db.session.commit()

            self.category_id  = category.id       # used by category & quiz tests
            self.question_id  = question.id         # used by delete test

            self.new_question = {
                "question": "Who invented Python?",
                "answer": "Guido van Rossum",
                "category": str(category.id),
                "difficulty": 2
            }
            self.search_payload = {"searchTerm": "H2O"}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Writing at least one test for each test for successful operation and for expected errors.
    """
    # Categories
    
    def test_get_categories_success(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data["categories"]))

    # Questions list woth pagination
    
    def test_get_paginated_questions_success(self):
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_get_questions_out_of_range_404(self):
        res = self.client().get("/questions?page=9999")
        self.assertEqual(res.status_code, 404)
        
    # Delete question

    def test_delete_question_success(self):
        res = self.client().delete(f"/questions/{self.question_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], self.question_id)

    def test_delete_question_not_found(self):
        res = self.client().delete("/questions/9999")
        self.assertEqual(res.status_code, 404)
        

    # Create question + bad request

    def test_create_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["created"])

    def test_create_question_400_missing_field(self):
        bad_payload = self.new_question.copy()
        bad_payload.pop("answer")
        res = self.client().post("/questions", json=bad_payload)
        self.assertEqual(res.status_code, 400)

    # Search
    
    def test_search_questions_success(self):
        res = self.client().post("/questions", json=self.search_payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["questions"]))
        self.assertIn("H2O", data["questions"][0]["question"])

    # Category based questions
    
    def test_get_questions_by_category_success(self):
        res = self.client().get(f"/categories/{self.category_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_category"], self.category_id)
        self.assertTrue(data["questions"])

    def test_get_questions_by_category_404(self):
        res = self.client().get("/categories/99/questions")
        self.assertEqual(res.status_code, 404)

    # The Quiz now

    def test_play_quiz_success(self):
        payload = {
            "previous_questions": [],
            "quiz_category": {"type": "Science", "id": str(self.category_id)},
        }
        res = self.client().post("/quizzes", json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["question"])

    def test_play_quiz_400_missing_previous(self):
        payload = {
            # missing "previous_questions"
            "quiz_category": {"type": "Science", "id": str(self.category_id)},
        }
        res = self.client().post("/quizzes", json=payload)
        self.assertEqual(res.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()