pipeline {
    agent any    
    
    stages {
        stage('Build') {
            parallel {
                stage('Backend') {
                    steps {
                        echo "Building backend docker"
                        dir('backend') {
                            sh 'docker build -t django-server'
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        echo "Building frontend docker"
                        dir('frontend') {
                            sh 'docker build'
                        }
                    }
                }
            }
        }
        stage('Test') {
            steps {
                echo "Running tests ..."
                sh '''
                    docker run --rm \
                    -e DJANGO_SETTINGS_MODULE=app.settings \
                    django-server \
                    poetry run python manage.py test characters.tests
                '''
            }
        }
        stage('Deploy') {
            when { 
                branch 'main'
            }
            steps {
            echo "Docker compose deploy"
                sh '''
                    docker compose down 
                    docker compose up -d --build
                '''
            }
        }
    }

    post {
        always {
             echo "Pipeline finished"
        }
        success {
            echo "Pipeline success"
        }
        failure {
            echo "Pipeline failure"
        }
        aborted {
            echo "Pipeline aborted"
        }
    }
}
