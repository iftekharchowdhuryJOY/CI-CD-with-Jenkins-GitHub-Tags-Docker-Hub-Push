pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iftekharchowdhury/flask-ci-app'
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/iftekharchowdhuryJOY/CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push.git'
            }
        }

        stage('Get Git Tag') {
            steps {
                script {
                    TAG = sh(script: "git describe --tags", returnStdout: true).trim()
                    env.IMAGE_TAG = "${TAG}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Image pushed: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "❌ Failed to push image"
        }
    }
}
