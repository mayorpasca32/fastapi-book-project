pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/mayorpasca32/fastapi-book-project.git'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    # Kill any process using port 8000 (if exists)
                    PID=$(lsof -ti :8000) && [ -n "$PID" ] && kill -9 $PID || echo "No process found on port 8000"

                    # Ensure dependencies are installed
                    pip3 install -r requirements.txt  

                    # Start Uvicorn in the background
                    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &  

                    # Wait for Uvicorn to start
                    sleep 5  

                    # Check if the server is running
                    curl -X GET -I http://127.0.0.1:8000/books/    
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    # Stop and remove old Docker container (if running)
                    docker stop fastapi-container || true
                    docker rm fastapi-container || true

                    # Build new Docker image
                    docker build -t fastapi-app .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    # Run new Docker container
                    docker run -d -p 8000:8000 --name fastapi-container fastapi-app
                '''
            }
        }
    }
}
