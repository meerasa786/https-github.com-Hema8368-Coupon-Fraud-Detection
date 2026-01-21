pipeline {
    agent any

    environment {
        DOCKERHUB = credentials('dockerhub-creds')
        DOCKER_USER = 'hsindhuja'
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Hema8368/Coupon-Fraud-Detection.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                docker build -t hsindhuja/cfd-api:latest api
                docker build -t hsindhuja/cfd-ml:latest ml
                docker build -t hsindhuja/cfd-ui:latest ui
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                sh '''
                echo $DOCKERHUB_PSW | docker login -u hsindhuja --password-stdin
                docker push hsindhuja/cfd-api:latest
                docker push hsindhuja/cfd-ml:latest
                docker push hsindhuja/cfd-ui:latest
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                sh '''
                docker compose down || true
                docker compose pull
                docker compose up -d
                '''
            }
        }
    }
}
