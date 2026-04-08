pipeline {
    agent any

    options {
        skipDefaultCheckout(true)   // avoid auto checkout
    }

    environment {
        SONAR_PROJECT_KEY = 'multi_ai_agent'
        SONAR_SCANNER_HOME = tool 'SonarQube'
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'mult_ai_agent'
        IMAGE_TAG = 'latest'
    }

    stages {

        stage('Checkout Code') {
            steps {
                cleanWs()   // prevents corruption
                checkout scm
            }
        }

        stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
                        docker push ${ecrUrl}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()   // cleanup after build
        }
    }
}