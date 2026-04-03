pipeline{
    agent any

    environment {
        SONAR_PROJECT_KEY = 'multi_ai_agent'
		SONAR_SCANNER_HOME = tool 'SonarQube'
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'mult_ai_agent'
        IMAGE_TAG = 'latest'
	}

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'multi_ai_agent', url: 'https://github.com/ANKUSHSINGH-PAT/Multi_AI_Agent.git']])
                }
            }
        }

    stage('SonarQube Analysis'){
			steps {
				withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
    					
					withSonarQubeEnv('SonarQube') {
    						sh """
						${SONAR_SCANNER_HOME}/bin/sonar-scanner \
						-Dsonar.projectKey=${SONAR_PROJECT_KEY} \
						-Dsonar.sources=. \
						-Dsonar.host.url=http://sonarqube-dind:9000 \
						-Dsonar.login=${SONAR_TOKEN}
						"""
					}
				}
			}
		}

    // stage('Build and Push Docker Image to ECR') {
    //         steps {
    //             withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
    //                 script {
    //                     def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
    //                     def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"

    //                     sh """
    //                     aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
    //                     docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
    //                     docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${ecrUrl}:${IMAGE_TAG}
    //                     docker push ${ecrUrl}:${IMAGE_TAG}
    //                     """
    //                 }
    //             }
    //         }
    //     }

    //     stage('Deploy to ECS Fargate') {
    // steps {
    //     withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
    //         script {
    //             sh """
    //             aws ecs update-service \
    //               --cluster multi-ai-agent-cluster \
    //               --service multi-ai-agent-def-service-shqlo39p  \
    //               --force-new-deployment \
    //               --region ${AWS_REGION}
    //             """
    //             }
    //         }
    //     }
    //  }

        // ─────────────────────────────────────────────────────────────────
        // Deploy to Kubernetes (EKS)
        // Pre-requisites on the Jenkins agent:
        //   • kubectl installed
        //   • AWS credentials that can call  eks:DescribeCluster
        //   • The EKS cluster name stored in Jenkins credential 'eks-cluster-name'
        //   • GROQ_API_KEY and TAVILI_API_KEY stored in Jenkins credentials
        // ─────────────────────────────────────────────────────────────────
        
    }
}
