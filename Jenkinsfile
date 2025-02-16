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
                        lsof -ti :${APP_PORT} | xargs -r kill -9 || true

                        pip3 install --no-cache-dir -r requirements.txt
                        pip3 install --no-cache-dir websockets  

                        cd ${WORKSPACE}  
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port ${APP_PORT} > fastapi.log 2>&1 &
                        sleep 10

                        if ! lsof -i :${APP_PORT}; then
                            cat fastapi.log  
                            exit 1
                        fi

                        if ! curl --retry 5 --retry-delay 2 -X GET -I http://127.0.0.1:${APP_PORT}/books/ | grep '200 OK'; then
                            cat fastapi.log  
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
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker build -t ${DOCKER_IMAGE} .
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh '''
                        echo "Checking for processes using port ${APP_PORT}..."
                        pkill -f "uvicorn" || true  # Kills any existing Uvicorn process
                        pkill -f "python3 -m uvicorn" || true  # Handles different command variations
                        sleep 3  # Give it time to stop
                
                        echo "Stopping any running Docker container..."
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                
                        echo "Starting new container..."
                        docker run -d --name fastapi-container -p 127.0.0.1:8000:8000 fastapi-app
                    '''
                }
             }
        }    
     }
}
