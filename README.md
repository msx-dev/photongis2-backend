To run this project

1. create a venv

2. pip install requirements

3. add .env file with

DATABASE_URL
JWT_SECRET=

4. run the DB with docker

5. run the backend inside the venv with
   python -m uvicorn main:app --reload (ensures it runs inside venv)
