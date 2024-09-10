# COSC-4353
Group 2

How to get the frontend running:

    Just go into frontend directory and do npm run dev.
    Server will be running on http://localhost:3000
    There's currently just some boiler plate front end stuff from React.


How to get the backend running:

    Create a python virtual environment in the backend directory.
    Do pip3 install -r requirements.txt to install dependencies.

    Now to start the server we first need to set our environment variables.
    Do export FLASK_APP=app.py
    and export FLASK_ENV=development

    then do flask run to run the server.
    use instead flask run --reload during development so changes are seen automatically.

    q + enter closes the server.

    Unix systems use export. If on windows type set instead of export.

    I set up some boiler plate backend to store user information.
    To see that it's working you can go to the url: http://127.0.0.1:5000/api/users

