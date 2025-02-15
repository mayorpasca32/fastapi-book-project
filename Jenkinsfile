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
                    pip3 install -r requirements.txt  # Ensure dependencies are installed
                    python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 &  # Use Python to launch Uvicorn
                    sleep 5  # Give it time to start
                    curl -X GET -I http://127.0.0.1:8000/books/    # Check if the server is running
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 8000:8000 fastapi-app'
            }
        }
    }
}
