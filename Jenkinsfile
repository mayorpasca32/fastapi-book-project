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
                        pip3 install --no-cache-dir -r requirements.txt

                        echo "Starting FastAPI server for tests..."
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port ${APP_PORT} > fastapi.log 2>&1 &
                        sleep 5

                        echo "Testing API Endpoint..."
                        if curl --retry 5 --retry-delay 2 -X GET -I http://127.0.0.1:${APP_PORT}/books/ | grep '200 OK'; then
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
                        /usr/bin/docker stop ${CONTAINER_NAME} || true
                        /usr/bin/docker rm ${CONTAINER_NAME} || true

                        echo "Checking if Docker is installed..."
                        if ! command -v /usr/bin/docker &> /dev/null; then
                            echo "Docker not found! Please install Docker first."
                            exit 1
                        fi

                        echo "Building Docker image..."
                        /usr/bin/docker build -t ${DOCKER_IMAGE} .
                        
                        echo "Verifying Docker image build..."
                        if /usr/bin/docker images | grep ${DOCKER_IMAGE}; then
                            echo "Docker image built successfully."
                        else
                            echo "Docker build failed!" && exit 1
                        fi
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        echo "Deploying container..."
                        /usr/bin/docker stop ${CONTAINER_NAME} || true
                        /usr/bin/docker rm ${CONTAINER_NAME} || true
                        /usr/bin/docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${DOCKER_IMAGE}
                        
                        echo "Verifying deployment..."
                        sleep 5
                        if /usr/bin/docker ps | grep ${CONTAINER_NAME}; then
                            echo "Container deployed successfully."
                        else
                            echo "Deployment failed!" && exit 1
                        fi
                    '''
                }
            }
        }
    }
}
