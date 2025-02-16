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
                        pip3 install --no-cache-dir websockets  

                        echo "Starting FastAPI server for tests..."
                        cd ${WORKSPACE}  # Ensure Jenkins is in the correct directory
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port ${APP_PORT} > fastapi.log 2>&1 &
                        sleep 10

                        echo "Checking if FastAPI is running..."
                        if ! lsof -i :${APP_PORT}; then
                            echo "FastAPI server failed to start!"
                            cat fastapi.log  # Print logs for debugging
                            exit 1
                        fi

                        echo "Testing API Endpoint..."
                        if curl --retry 5 --retry-delay 2 -X GET -I http://127.0.0.1:${APP_PORT}/books/ | grep '200 OK'; then
                            echo "Test passed!"
                        else
                            echo "Test failed!" 
                            cat fastapi.log  # Print logs for debugging
                            exit 1
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
                        if ! /usr/bin/docker --version &> /dev/null; then
                            echo "Docker not found! Please install Docker first."
                            exit 1
                        fi

                        echo "Checking user and groups for debugging..."
                        whoami
                        groups
                        command -v docker || echo "Docker not found!"
                        docker info || echo "Docker command failed!"

                        echo "Building Docker image..."
                        /usr/bin/docker stop ${CONTAINER_NAME} || true
                        /usr/bin/docker rm ${CONTAINER_NAME} || true
                        /usr/bin/docker build -t ${DOCKER_IMAGE} .
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
