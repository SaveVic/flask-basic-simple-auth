# Flask Simple Auth
Using Flask to build web app for simple user authentication and authorization.

## Extension
- SQL ORM: [<u>SQLAlchemy</u>](https://docs.sqlalchemy.org/en/20/)
- Testing: [<u>Pytest</u>](https://docs.pytest.org/en/7.4.x/)

## Installation 
Clone from the repository:
```
$ git clone https://github.com/SaveVic/flask-basic-simple-auth.git
```

Create a virtualenv and activate it::
```
$ python3 -m venv .venv
$ . .venv/bin/activate
```
    
Or on Windows cmd::
```
$ py -3 -m venv .venv
$ .venv\Scripts\activate.bat
```

Install requirements with pip:
```
$ pip install -r requirements.txt
```

Install the app:
```
$ pip install -e .
```

## Run

### Run for developing
```
$ flask --app flaskr run -p [port] -h [host] --debug
```
- -p : port, default `5000`
- -h : host address, default `127.0.0.1`

Open [<u>http://[host]:[port]</u>](http://host:port) in your browser.

### Run for testing
```
$ pytest
```

Run with coverage report:
```
$ coverage run -m pytest
$ coverage report
$ coverage html
```   
Open [<u>htmlcov/index.html</u>](htmlcov/index.html) in a browser.