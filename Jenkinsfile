pipeline {
    agent any

    environment {
        // Use YOUR Docker Hub username (must match credentials)
        IMAGE_NAME = 'monnomestjoy/flask-ci-app'  
    }

    stages {
        stage('Clone & Prepare') {
            steps {
                cleanWs()  // Clean workspace first
                script {
                    // Clone repo
                    sh '''
                        git clone https://github.com/iftekharchowdhuryJOY/CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push.git
                    '''
                    
                    // Get latest tag and checkout
                    dir('CI-CD-with-Jenkins-GitHub-Tags-Docker-Hub-Push') {
                        env.IMAGE_TAG = sh(
                            script: "git fetch --tags && git describe --tags `git rev-list --tags --max-count=1`", 
                            returnStdout: true
                        ).trim()
                        sh "git checkout ${env.IMAGE_TAG}"
                        
                        // Copy files to workspace root
                        sh "cp -r . ../"  
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build --no-cache -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([[
                    $class: 'UsernamePasswordMultiBinding',
                    credentialsId: 'docker-hub',  // Verify this credential exists in Jenkins
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                ]]) {
                    sh '''
                        # Login to Docker Hub
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        
                        # Push the image
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                        
                        # Logout (security best practice)
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Success! Pushed ${IMAGE_NAME}:${IMAGE_TAG} to Docker Hub"
        }
        failure {
            echo "❌ Pipeline failed - check logs above"
        }
    }
}