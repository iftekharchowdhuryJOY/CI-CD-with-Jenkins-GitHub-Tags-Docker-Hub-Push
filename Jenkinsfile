pipeline {
    agent any

    environment {
        // ✅ Confirm this EXACTLY matches your Docker Hub username
        IMAGE_NAME = 'monnomestjoy/flask-ci-app'  
    }

    stages {
        stage('Clone & Prepare') {
            steps {
                cleanWs()  // Clean workspace to avoid conflicts
                script {
                    // Clone repo (replace with your actual Git URL)
                    sh '''
                        git clone https://github.com/iftekharchowdhuryJOY/CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push.git
                    '''
                    
                    // Get the latest Git tag
                    dir('CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push') {
                        env.IMAGE_TAG = sh(
                            script: "git fetch --tags && git describe --tags `git rev-list --tags --max-count=1`", 
                            returnStdout: true
                        ).trim()
                        sh "git checkout ${env.IMAGE_TAG}"
                        sh "cp -r . ../"  // Copy files to workspace root
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    # Pull base image first to avoid rate limits
                    docker pull python:3.10-slim || true
                    
                    # Build with --no-cache to avoid layer conflicts
                    docker build --no-cache -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    
                    # Verify the image was created
                    docker images | grep '${IMAGE_NAME}'
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([[
                    $class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'docker-hub',  // ✅ Must match Jenkins credential ID
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                ]]) {
                    sh '''
                        # Login to Docker Hub
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        
                        # Push with retry (in case of network issues)
                        docker push ${IMAGE_NAME}:${IMAGE_TAG} || {
                            echo "First push failed. Retrying in 10 seconds...";
                            sleep 10;
                            docker push ${IMAGE_NAME}:${IMAGE_TAG};
                        }
                        
                        # Logout for security
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Success! Pushed ${IMAGE_NAME}:${IMAGE_TAG} to Docker Hub"
            sh """
                echo "Verify at: https://hub.docker.com/r/monnomestjoy/flask-ci-app/tags"
            """
        }
        failure {
            echo "❌ Pipeline failed - check logs above"
            sh "docker logout"  // Force logout on failure
        }
    }
}