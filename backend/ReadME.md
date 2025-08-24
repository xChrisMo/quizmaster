# Trivia API DOcumentation

## Base URL

Local dev (default): `http://127.0.0.1:5000/`

> All endpoints return **JSON** and accept/return `Content-Type: application/json`.  
> Pagination page size is exaclty **10**; we use the `page` query-param where noted.

## Endpoints

### `GET /categories`

| Code | Meaning                    |
|------|----------------------------|
| 200  | Success. Returns all categories |


{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "...": "..."
  }
}


### `GET /questions?page=<int>`
Fetches paginated questions and a categories map.

Query	Type	Default	Notes
page	int	1	1-indexed

Code - Meaning
200	- Page contains questions
404	- Page empty (e.g., page 9999)


{
  "success": true,
  "questions": [ { "...": "..." }, ... ],
  "total_questions": 54,
  "current_category": null,
  "categories": { "1": "Science", ... }
}


### `DELETE /questions/<int:question_id>`
Code - Meaning
200	- Question deleted
404	- ID not found


{
  "success": true,
  "deleted": 17,
  "questions": [ { "...": "..." } ],
  "total_questions": 53
}


### `POST /questions`

1. Dual-purpose endpoint:

2. Search when body contains searchTerm


#### Search payload

{ "searchTerm": "title" }
Code - Meaning
200 - Success (array may be empty)

{
  "success": true,
  "questions": [ { "id": 3, "question": "Movie title...", ... } ],
  "total_questions": 1,
  "current_category": null
}
                
#### Create payload

{
  "question": "Who invented Python?",
  "answer":   "Guido van Rossum",
  "category": "1",
  "difficulty": 2
}
Code - Meaning
200	- Question created
400	- Missing required field



{
  "success": true,
  "created": 55,
  "questions": [ { "...": "..." } ],
  "total_questions": 55
}

### `GET /categories/<int:id>/questions`

Code - Meaning
200	- Success
404	- Category not found


{
  "questions": [ { "...": "..." } ],
  "total_questions": 18,
  "current_category": 1
}

### `POST /quizzes`
Returns one random question not yet asked.

Payload schema
Field	Type	Description
previous_questions	list<int>	IDs already shown
quiz_category	object	{ "id": "0", "type": "click" } for All or { "id": "3", "type": "Science" }

Code - Meaning
200	- Success; "question" is null if none left
400	- Missing previous_questions key


// 200 with next question
{
  "success": true,
  "question": { "id": 23, "question": "...", "answer": "...", "category": "1", "difficulty": 1 }
}

// 200 when exhausted
{
  "success": true,
  "question": null
}

Error Format
{
  "success": false,
  "error": 404,
  "message": "Page not found"
}
Codes used: 400, 404, 405, 422, 500.













## Quick-start (local)


#### 1. Clone & install
* git clone [this link](https://github.com/udacity/cd0037-API-Development-and-Documentation-project)

* cd trivia_api

* pip install -r requirements.txt   # or use pipenv / venv alternatives

#### 2. PostgreSQL (example)
* createdb trivia

* createdb trivia_test

#### 3. Run the app
* export FLASK_APP=flaskr

* flask run

#### 4. Run tests
* python test_flaskr.py














## Example cURL


### All categories
* curl localhost:5000/categories

#### Create a question
* curl -X POST localhost:5000/questions \
       -H "Content-Type: application/json" \
       -d '{"question":"Who?", "answer":"Me", "category":"1", "difficulty":1}'

#### Search for "H2O"
* curl -X POST localhost:5000/questions \
       -H "Content-Type: application/json" \
       -d '{"searchTerm":"H2O"}'

#### Play quiz (Science, skipping IDs 12 & 17)
* curl -X POST localhost:5000/quizzes \
       -H "Content-Type: application/json" \
       -d '{"previous_questions":[12,17],"quiz_category":{"id":"1","type":"Science"}}'