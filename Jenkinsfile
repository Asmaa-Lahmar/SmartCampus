pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -la'
                sh 'git log -1 --oneline'
            }
        }
    }
}
