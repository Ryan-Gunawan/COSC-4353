# COSC-4353
Group 2

How to get the frontend running:

cd into frontend directory and install dependencies:

    npm install

run the server in development mode:

    npm run dev

Server will be running on http://localhost:3000


How to get the backend running:

Navigate to the backend directory:

    cd backend

Create a virtual environment:

- On Mac/Linux:

```bash
    python3 -m venv venv
```

- On Windows:

```bash
    python -m venv venv
```

Activate the virtual environment:

- On Mac/Linux:

```bash
    source venv/bin/activate
```

- On Windows:

```bash
    venv\Scripts\activate
```

Install the dependencies

- On Mac/Linux:

```bash
    pip3 install -r requirements.txt
```

- On Windows:

```bash
    pip install -r requirements.txt
```

Set our environment variables for the server

- On Mac/Linux:

```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
```

- On Windows:

```bash
    set FLASK_APP=app.py
    set FLASK_ENV=development
```

Run the flask app server

    flask run

- during development so changes are seen automatically.

```bash
    flask run --reload 
```
    q + enter closes the server.

I set up some boiler plate backend to store user information.
To see that it's working you can go to the url: http://127.0.0.1:5000/api/users


***Teddy's note***
Run the backend server with bash:
    --- cd backend
    --- python -m flask run
Terminate program to reflect new changes to the code.

For frontend development:
    Activate the virtual environment, which has all the requiremnet installed.
        --- venv\Scripts\activate
    Then in the powershell:
        --- npm run dev

For database dev:
    To activate flask shell: 
        --- $ python -m flask shell

    To see table names:
        --- from app import db
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(tables)
            
    To see columns of a specific table (e.g., 'event'):
        --- print(inspector.get_columns('event'))

    To see all the contents of the table:
        from app import Event
        events = Event.query.all()
        for event in events:
            print(event)
