pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            cd backend
                            python3 -m venv .venv
                            . .venv/bin/activate
                            pip install -r requirements.txt
                        '''
                        sh 'cd frontend && npm ci && npm run build'
                    } else {
                        bat '''
                            cd backend
                            python -m venv .venv
                            call .venv\\Scripts\\activate.bat
                            pip install -r requirements.txt
                        '''
                        bat 'cd frontend && npm ci && npm run build'
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'cd backend && . .venv/bin/activate && pytest'
                        sh 'cd frontend && CI=true npm test -- --run'
                    } else {
                        bat 'cd backend && call .venv\\Scripts\\activate.bat && pytest'
                        bat 'cd frontend && set CI=true && npm test -- --run'
                    }
                }
            }
        }
    }
}
