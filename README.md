This microservice 

Requirements
- Python 3.11+
- Docker Desktop (https://www.docker.com/products/docker-desktop/)

Setup

Clone the repo and open a terminal in the project folder

Create and activate a virtual environment
Windows: 
    
        python -m venv venv  
        venv\Scripts\activate
        
Mac and Linux: 
        
        python -m venv venv
        venv/bin/activate

 pip install -r requirements.txt
 
 docker compose up postgres -d
 
 uvicorn app.main:app --reload --port 8000

The API is now running at http://localhost:8000/docs

Credit Declan Littleton 2026