# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Reference

### Getting started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

### Error handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API return 4 error types when request fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

### Endpoints. 

#### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample :  ``` curl -X GET http://localhost:5000/categories```
```
{
    "categories": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "success": true
}
```

#### GET '/questions'
- Fetches a dictionary of questions in which the keys are the ids
- Request Arguments: None
- Returns: An object with questions, categories, and total of questions. 
- Sample :  ``` curl -X GET http://localhost:5000/questions```

```
{
    "categories": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
    "current_category": "entertainment",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        .....
    "success": true,
    "total_questions": 19
```

#### GET '/categories/{category_id}/questions'
- Fetches all the questions  of a category
- Request Arguments: category_id
- Returns: An object with all the questions of the category requested. 
- Sample :  ``` curl -X GET http://localhost:5000/categories/5/questions```
```
{
    "current_category": "Entertainment",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        ......
    "success": true,
    "total_question": 3
```


#### POST '/questions'
- Create a new questions using question, answer, category and difficulty
- Returns: Id of the new question. 
- Sample :
```
curl -X POST http://localhost:5000/questions \
  -H 'Content-Type: application/json' \
  -d '{"question":"Who is the King of Pop?", "answer":"Michael Jackson", "category":"2", "difficulty":"5"}'
```
- Response:
```
{
    "question_id": 25,
    "success": true
}
```
#### POST '/questions' for search
- Fetches all the questions that match with a search term
- Returns: An object with all the questions matched with the search

```
curl -X POST http://localhost:5000/questions \
  -H 'Content-Type: application/json' -d '{"searchTerm":"Pop"}'
```
- Response:

```
{
    "current_category": "entertainment",
    "questions": [
        {
            "answer": "Michael Jackson",
            "category": 5,
            "difficulty": null,
            "id": 25,
            "question": "Who is the King of Pop?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
#### POST '/quizzes'
- Get questions to play the quiz. This endpoint take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
-  Sample:

```
curl -X POST http://localhost:5000/quizzes \
  -H 'Content-Type: application/json' \
  -d '{
    "quiz_category": {
        "id": 1
    },
    "previous_questions": [
        20
    ]
}'
```
- Response
```
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}

```

#### DELETE '/questions/{question_id}'
- DELETE question using a question ID.
- Sample: ``` curl -X DELETE http://localhost:5000/questions/5```

```
{
    'success': True
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```