pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/mayorpasca32/fastapi-book-project.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'pytest'
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

