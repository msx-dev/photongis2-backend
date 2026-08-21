To run this project

1. create a venv

2. pip install requirements

3. add .env file with

DATABASE_URL
JWT_SECRET=

4. run the DB with docker

5. run the backend inside the venv with
   python -m uvicorn main:app --reload (ensures it runs inside venv)

Additional:

1. Whenever you change the manual, for RAG run the indexer:
   python -m tests.test_indexer

This will replace the chunks with new ones

2. To save space on server, indexing should be done locally and chroma_data pushed to server
   If you want to run indexing when starting the application, uncomment the index_manual() function in main.py lifespan
