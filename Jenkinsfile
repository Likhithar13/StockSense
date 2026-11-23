pipeline {
  agent any
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Install') {
      steps { sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt' }
    }
    stage('Test') {
      steps { sh '. .venv/bin/activate && pytest --cov=app --cov=services' }
    }
    stage('Build Docker image') {
      steps { sh 'docker build -t stocksense:${BUILD_NUMBER} .' }
    }
  }
  post { always { junit allowEmptyResults: true, testResults: 'reports/*.xml' } }
}
