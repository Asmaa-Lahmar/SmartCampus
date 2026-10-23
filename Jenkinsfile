pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm

                script {
                    if (isUnix()) {
                        sh 'ls -la'
                        sh 'git log -1 --oneline'
                    } else {
                        bat 'dir'
                        bat 'git log -1 --oneline'
                    }
                }
            }
        }
    }
}
