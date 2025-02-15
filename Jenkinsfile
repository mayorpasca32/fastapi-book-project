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
                        echo "Stopping any process using port ${APP_PORT}..."
                        lsof -ti :${APP_PORT} | xargs -r kill -9 || true

                        echo "Installing dependencies..."
                        pip3 install -r requirements.txt

                        echo "Starting FastAPI server for tests..."
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port ${APP_PORT} > fastapi.log 2>&1 &
                        sleep 5

                        echo "Testing API Endpoint..."
                        if curl -X GET -I http://127.0.0.1:${APP_PORT}/books/ | grep '200 OK'; then
                            echo "Test passed!"
                        else
                            echo "Test failed!" && exit 1
                        fi
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        echo "Stopping existing container if running..."
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true

                        echo "Checking if Docker is installed..."
                        if ! command -v docker &> /dev/null; then
                            echo "Docker not found! Please install Docker first."
                            exit 1
                        fi

                        echo "Building Docker image..."
                        docker build -t ${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        echo "Deploying container..."
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}
                    '''
                }
            }
        }
    }
}
