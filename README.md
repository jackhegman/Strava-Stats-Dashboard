# Strava-Stats-Dashboard

Mac OSX / Linux

In the root directory run:

1. python3 -m venv env
2. source env/bin/activate && touch .env
3. pip install -r requirements.txt
4. Add the STRAVA_SECRET_KEY=xxxx and STRAVA_CLIENT_ID=xxxx into the .env file at the root of the folder
4. python manage.py migrate && python manage.py runserver

In a new terminal run:
1. cd frontend && npm install && npm start


Windows

In the root directory run the following with cmd:

1. python3 -m venv env
2. env\Scripts\activate.bat && type nul > .env
3. pip install -r requirements.txt
4. Add the STRAVA_SECRET_KEY=xxxx and STRAVA_CLIENT_ID=xxxx into the .env file at the root of the folder
4. python manage.py migrate && python manage.py runserver

In a new terminal run:
1. cd frontend && npm install && npm start