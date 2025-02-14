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
                sh 'pip3 install -r requirements.txt'
                sh 'uvicorn main:app --host 0.0.0.0 --port 8000 &'
                sh 'sleep 5'  // Allow time for the server to start
                sh 'curl -I http://127.0.0.1:8000/books/'  // Check if it's running
                sh 'python3 -m pytest'
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
