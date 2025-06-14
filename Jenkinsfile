pipeline {
    agent {
        docker {
            image 'your-dockerhub-username/task-manager-image'
            args '-u root'  // to avoid permission issues
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'python tests/test_app.py'
            }
        }
    }
}
