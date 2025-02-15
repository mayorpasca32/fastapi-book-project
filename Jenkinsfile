pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "fastapi-app"
        CONTAINER_NAME = "fastapi-container"
        APP_PORT = "8000"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        lsof -ti :${APP_PORT} | xargs -r kill -9
                        pip3 install -r requirements.txt
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port ${APP_PORT} &
                        sleep 5
                        curl -X GET -I http://127.0.0.1:${APP_PORT}/books/
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker buildx create --use || true
                        docker build --progress=plain -t ${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}
                    '''
                }
            }
        }
    }
}
