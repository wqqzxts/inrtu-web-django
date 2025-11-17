pipeline {
    agent any    
    
    stages {
        stage('Build') {
            parallel {
                stage('Backend') {
                    steps {
                        echo "Building backend docker"
                        dir('backend') {
                            sh 'docker build -t django-server .'
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        echo "Building frontend docker"
                        dir('frontend') {
                            sh 'docker build -t vue-server .'
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
                    docker compose down || true
                    docker compose up -d --build
                    sleep 30
    
                    docker exec django-server poetry python manage.py makemigrations
                    docker exec django-server poetry python manage.py migrate
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
