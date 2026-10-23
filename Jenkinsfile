pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm

                script {
                    if (isUnix()) {
                        sh 'git log -1 --oneline'
                    } else {
                        bat 'git log -1 --oneline'
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv backend/.venv
                            backend/.venv/bin/python -m pip install -r backend/requirements.txt
                            backend/.venv/bin/python -m pip install pytest
                            backend/.venv/bin/python -m compileall -q backend/src
                        '''
                    } else {
                        bat '''
                            py -3 -m venv backend\\.venv
                            backend\\.venv\\Scripts\\python.exe -m pip install -r backend\\requirements.txt
                            backend\\.venv\\Scripts\\python.exe -m pip install pytest
                            backend\\.venv\\Scripts\\python.exe -m compileall -q backend\\src
                        '''
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            cd frontend
                            npm ci
                            npm run build
                        '''
                    } else {
                        bat '''
                            cd frontend
                            call npm ci
                            call npm run build
                        '''
                    }
                }
            }
        }

        stage('Test Backend') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'backend/.venv/bin/python -m pytest backend -v'
                    } else {
                        bat 'backend\\.venv\\Scripts\\python.exe -m pytest backend -v'
                    }
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'frontend/dist/**',
                             fingerprint: true,
                             allowEmptyArchive: true
        }
    }
}
