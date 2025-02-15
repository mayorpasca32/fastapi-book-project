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

                        # Ensure Docker Buildx is available
                        docker buildx version || {
                            echo "Docker Buildx is missing. Installing..."
                            mkdir -p ~/.docker/cli-plugins
                            curl -L https://github.com/docker/buildx/releases/latest/download/buildx-linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
                            chmod +x ~/.docker/cli-plugins/docker-buildx
                        }

                        # Use Buildx with the default builder
                        docker buildx create --use --name mybuilder || true
                        docker buildx use mybuilder

                        # Build the image using Buildx
                        DOCKER_BUILDKIT=1 docker buildx build --platform linux/amd64 -t ${DOCKER_IMAGE} .
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
