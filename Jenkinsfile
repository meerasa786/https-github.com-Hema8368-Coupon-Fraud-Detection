pipeline {
  agent any

  environment {
    DOCKERHUB_CREDS = 'dockerhub-creds'
    DOCKER_USER = 'meera786'
    TAG = 'latest'
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
          '''
        }
      }
    }

    stage('Deploy (Run Containers)') {
      steps {
        sh '''
          docker rm -f fraud-api fraud-ml fraud-admin fraud-checkout || true

          docker pull $DOCKER_USER/fraud-api:$TAG
          docker pull $DOCKER_USER/fraud-ml:$TAG
          docker pull $DOCKER_USER/fraud-admin:$TAG
          docker pull $DOCKER_USER/fraud-checkout:$TAG

          docker run -d --name fraud-api -p 5000:5000 $DOCKER_USER/fraud-api:$TAG
          docker run -d --name fraud-ml -p 8000:8000 $DOCKER_USER/fraud-ml:$TAG
          docker run -d --name fraud-admin -p 8080:8080 $DOCKER_USER/fraud-admin:$TAG
          docker run -d --name fraud-checkout -p 8081:8080 $DOCKER_USER/fraud-checkout:$TAG
        '''
      }
    }
  }

  post {
    always {
      sh 'docker system prune -f || true'
    }
  }
}
