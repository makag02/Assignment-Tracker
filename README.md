# Assignment-Tracker
Assignment tracking REST API built with FastAPI, SQLAlchemy, and SQLite

A RESTful backend service for managing academic courses and assignments. 
Built with FastAPI and SQLAlchemy, the application supports task creation, filtering, completion tracking, and summary analytics with persistent SQLite storage.
Uses SwaggerUI for a UI

To run
Clone the repo.

In terminal:

  Create python venv and install dependencies with:
  
  py -m venv .venv
  
  .\.venv\Scripts\Activate.ps1
  
  py -m pip install --upgrade pip
  
  pip install fastapi uvicorn sqlalchemy pydantic
  
  Start the server:
  
  uvicorn app.main:app --reload

  Open website:
  http://127.0.0.1:8000/docs

Within SwaggerUI you can use the drop downs for the courses and assignments table then click "try it out" to attempt to load data or execute queries
