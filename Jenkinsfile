def runCmd(String linuxCommand, String windowsCommand) {
    if (isUnix()) {
        sh linuxCommand
    } else {
        bat windowsCommand
    }
}

pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }
    environment {
        TEST_DATABASE_URL = 'postgresql+psycopg://smartcampus:smartcampus@localhost:5432/smartcampus_test'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                dir('backend') {
                    script {
                        runCmd('python3 -m venv .venv', 'python -m venv .venv')
                        runCmd('.venv/bin/python -m pip install -r requirements-dev.txt',
                               '.venv\\Scripts\\python -m pip install -r requirements-dev.txt')
                        runCmd('.venv/bin/python -m compileall -q src',
                               '.venv\\Scripts\\python -m compileall -q src')
                    }
                }
                dir('frontend') {
                    script {
                        runCmd('npm ci', 'npm ci')
                        runCmd('npm run build', 'npm run build')
                    }
                }
                script {
                    runCmd('rm -rf dist', 'if exist dist rmdir /s /q dist')
                    runCmd('mkdir dist', 'mkdir dist')
                    runCmd('tar -czf dist/smartcampus-api-${BUILD_NUMBER}.tar.gz --exclude=__pycache__ -C backend src migrations alembic.ini requirements.txt',
                           'tar -czf dist\\smartcampus-api-%BUILD_NUMBER%.tar.gz --exclude=__pycache__ -C backend src migrations alembic.ini requirements.txt')
                    runCmd('tar -czf dist/smartcampus-web-${BUILD_NUMBER}.tar.gz -C frontend/dist .',
                           'tar -czf dist\\smartcampus-web-%BUILD_NUMBER%.tar.gz -C frontend\\dist .')
                }
            }
        }
        stage('Test') {
            steps {
                dir('backend') {
                    script {
                        runCmd('.venv/bin/python -m pytest --junitxml=reports/junit.xml --cov-report=xml:reports/coverage.xml',
                               '.venv\\Scripts\\python -m pytest --junitxml=reports\\junit.xml --cov-report=xml:reports\\coverage.xml')
                    }
                }
            }
        }
    }
    post {
        always {
            junit testResults: 'backend/reports/junit.xml', allowEmptyResults: true
        }
        success {
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
        }
    }
}
