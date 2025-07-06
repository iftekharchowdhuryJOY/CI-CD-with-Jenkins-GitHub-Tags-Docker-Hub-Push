pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iftekharchowdhury/flask-ci-app'
    }

    stages {
        stage('Clone') {
            steps {
                script {
                    sh '''
                        rm -rf CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push || true
                        git clone https://github.com/iftekharchowdhuryJOY/CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push.git
                    '''
                }

                script {
                    // Enter repo folder and find latest tag using Groovy
                    dir('CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push') {
                        env.IMAGE_TAG = sh(script: "git fetch --tags && git describe --tags `git rev-list --tags --max-count=1`", returnStdout: true).trim()
                        sh "git checkout ${env.IMAGE_TAG}"
                    }

                    // Copy the tagged contents back to Jenkins workspace
                    sh '''
                        cp -r CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push/* .
                    '''
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
