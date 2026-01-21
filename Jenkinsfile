pipeline {
  agent any

  environment {
    DOCKERHUB_CREDS = 'dockerhub-creds'
    DOCKER_USER = 'meera786'
    TAG = 'latest'
    DEPLOY_DIR = '/opt/fraud-deploy'
    COMPOSE_FILE = '/opt/fraud-deploy/docker-compose.yml'
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build Images') {
      steps {
        sh '''
          docker build -t $DOCKER_USER/fraud-api:$TAG -f api/Dockerfile api
          docker build -t $DOCKER_USER/fraud-ml:$TAG -f ml/Dockerfile ml
          docker build -t $DOCKER_USER/fraud-admin:$TAG -f apps/admin/Dockerfile apps/admin
          docker build -t $DOCKER_USER/fraud-checkout:$TAG -f apps/checkout/Dockerfile apps/checkout
        '''
      }
    }

    stage('Push to Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDS, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin

            docker push $DOCKER_USER/fraud-api:$TAG
            docker push $DOCKER_USER/fraud-ml:$TAG
            docker push $DOCKER_USER/fraud-admin:$TAG
            docker push $DOCKER_USER/fraud-checkout:$TAG

            docker logout || true
          '''
        }
      }
    }

    stage('Deploy from Docker Hu
