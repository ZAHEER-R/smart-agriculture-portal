pipeline {
    agent any
 
    parameters {
        string(name: 'IMAGE_TAG', defaultValue: 'v1', description: 'Docker image tag')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'prod'], description: 'Target environment')
    }
 
    environment {
        DOCKERHUB_USER = '<your-dockerhub-username>'
        IMAGE_NAME     = "${DOCKERHUB_USER}/smart-agri-portal"
    }
 
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/<your-username>/smart-agriculture-portal.git'
            }
        }
 
        stage('Build & Test') {
            parallel {
                stage('Build Docker Image') {
                    steps {
                        sh "docker build -t ${IMAGE_NAME}:${params.IMAGE_TAG} ."
                    }
                }
                stage('Unit Smoke Test') {
                    steps {
                        sh '''
                          python -c "import json; json.load(open('app/data/fields.json'))"
                          echo "JSON data validation passed"
                        '''
                    }
                }
            }
        }
 
        stage('Push to Docker Hub') {
            when {
                expression { params.ENVIRONMENT == 'prod' }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS')]) {
                    sh '''
                      echo $PASS | docker login -u $USER --password-stdin
                      docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }
 
        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                  kubectl set image deployment/smart-agri-portal \
                    portal=${IMAGE_NAME}:${IMAGE_TAG} --record || \
                  kubectl apply -f k8s/
                  kubectl rollout status deployment/smart-agri-portal
                '''
            }
        }
    }
 
    post {
        always {
            archiveArtifacts artifacts: '**/Dockerfile,**/Jenkinsfile,k8s/**', allowEmptyArchive: true
        }
        success {
            echo "Pipeline completed successfully for tag ${params.IMAGE_TAG}"
        }
        failure {
            echo "Pipeline failed – check logs"
        }
    }
}
