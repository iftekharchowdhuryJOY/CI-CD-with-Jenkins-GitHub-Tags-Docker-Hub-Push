pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-ci-app'
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/iftekharchowdhuryJOY/CI-CD-Project-Using-JENKINS.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export PYTHONPATH=$PWD
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Get Git Tag') {
            steps {
                script{
                    TAG = sh(script: "git describe --tags", returnStdout: true).trim()
                    env.IMAGE_TAG = "${TAG}"
                }
            }
        }
        stage('Deploy to Dev') {
            steps {
                sh '''
                    docker stop flask-dev || true && docker rm flask-dev || true
                    docker run -d --name flask-dev -p 5001:5000 flask-ci-app:dev
                '''
            }
        }

       stage('Promote to Staging') {
    steps {
        script {
            input message: '🚀 Promote to staging?', ok: 'Promote'
        }
        sh '''
            docker tag flask-ci-app:dev flask-ci-app:staging
            docker stop flask-staging || true && docker rm flask-staging || true
            docker run -d --name flask-staging -p 5002:5000 flask-ci-app:staging
        '''
    }
}

    }

    post {
        always {
            echo '🚦 Pipeline finished.'
        }
        success {
            echo '✅ All stages passed!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
