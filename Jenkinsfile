// Pipeline d'intégration continue de SmartCampus - TP 3, partie 3
// Checkout -> Build -> Test, sur un agent Jenkins Linux (sh) ou Windows (bat).
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
            }
        }
        stage('Test') {
            steps {
                dir('backend') {
                    // pytest.ini ajoute la couverture et échoue sous 70 % (ENF-11)
                    run('.venv/bin/python -m pytest', '.venv\\Scripts\\python -m pytest')
                }
            }
        }
    }
}
// Lance la commande Linux sur un agent Linux, la commande Windows sinon
def run(String linuxCommand, String windowsCommand) {
    if (isUnix()) {
        sh linuxCommand
    } else {
        bat windowsCommand
    }
}
