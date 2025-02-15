pipeline {
    agent any

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
                        echo "Stopping any process using port 8000..."
                        lsof -ti :8000 | xargs -r kill -9

                        echo "Installing dependencies..."
                        pip3 install --no-cache-dir -r requirements.txt
                        pip3 install --no-cache-dir websockets  # Ensure 'websockets' is installed

                        echo "Starting FastAPI server for tests..."
                        nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
                        sleep 10  # Give time for the server to start

                        echo "Checking if FastAPI is running..."
                        if ! lsof -i :8000; then
                            echo "FastAPI server failed to start!"
                            cat fastapi.log
                            exit 1
                        fi

                        echo "Running Tests..."
                        pytest --maxfail=1 --disable-warnings --tb=short
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            when {
                not {
                    failed()
                }
            }
            steps {
                script {
                    sh 'docker build -t fastapi-book-project .'
                }
            }
        }

        stage('Deploy') {
            when {
                not {
                    failed()
                }
            }
            steps {
                script {
                    sh 'docker run -d -p 80:8000 fastapi-book-project'
                }
            }
        }
    }
}
