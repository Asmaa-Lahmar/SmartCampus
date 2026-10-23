pipeline {
    agent any
    options {
        // Le stage Checkout ci-dessous récupère le code : pas de checkout automatique en double
        skipDefaultCheckout(true)
    }
    environment {
        // Base PostgreSQL des tests : son nom doit finir par _test (voir backend/tests/conftest.py)
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
                    // Environnement Python du build et dépendances (API + outils de test)
                    run('python3 -m venv .venv', 'python -m venv .venv')
                    run('.venv/bin/python -m pip install -r requirements-dev.txt',
                        '.venv\\Scripts\\python -m pip install -r requirements-dev.txt')
                    // Vérifie que tout le code Python se compile (erreurs de syntaxe)
                    run('.venv/bin/python -m compileall -q src', '.venv\\Scripts\\python -m compileall -q src')
                }
                dir('frontend') {
                    // Installe les versions exactes du package-lock.json puis compile React + TypeScript
                    run('npm ci', 'npm ci')
                    run('npm run build', 'npm run build')
                }
                // Archives du build, numérotées : l'équivalent du .jar de Maven
                run('rm -rf dist', 'if exist dist rmdir /s /q dist')
                run('mkdir dist', 'mkdir dist')
                run('tar -czf dist/smartcampus-api-${BUILD_NUMBER}.tar.gz --exclude=__pycache__ -C backend src 
migrations alembic.ini requirements.txt',
                    'tar -czf dist\\smartcampus-api-%BUILD_NUMBER%.tar.gz --exclude=__pycache__ -C backend src 
migrations alembic.ini requirements.txt')
                run('tar -czf dist/smartcampus-web-${BUILD_NUMBER}.tar.gz -C frontend/dist .',
                    'tar -czf dist\\smartcampus-web-%BUILD_NUMBER%.tar.gz -C frontend\\dist .')
            }
        }
        stage('Test') {
            steps {
                dir('backend') {
                    // Rapport JUnit pour Jenkins et rapport de couverture XML (réutilisable par SonarQube)
                    run('.venv/bin/python -m pytest --junitxml=reports/junit.xml --cov
report=xml:reports/coverage.xml',
                        '.venv\\Scripts\\python -m pytest --junitxml=reports\\junit.xml --cov
report=xml:reports\\coverage.xml')
                }
            }
        }
    }
    post {
        always {
            // Résultats des tests visibles dans Jenkins, même quand un test échoue
            junit testResults: 'backend/reports/junit.xml', allowEmptyResults: true
        }
        success {
            // Conservé uniquement si le pipeline réussit : point d'entrée du TP Docker
            archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
        }
    }
}

def run(String linuxCommand, String windowsCommand) {
