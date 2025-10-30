pipeline {
    agent any

    stage('Build') {
        parallel {
            stage('Backend') {
                steps {
                    echo "Build for backend ..."
                    bat '''
                        conda activate base
                        conda env create -f enironment.yml
                        conda activate inrtu-web-django

                        python manage.py makemigrations
                        python manage.py migrate                        
                    '''
                }
            }
            stage('Frontend') {
                steps {
                    echo "Build for frontend ..."
                    bat '''
                        cd client
                        npm install                        
                    '''
                }
            }
        }
    }
    stage('Test') {
        steps {
            echo "Running tests ..."            
        }
    }
    stage('Deploy') {
        parallel {
            stage('Backend') {
                steps {
                    echo "Deploy for backend ..."
                    bat ```
                        conda activate inrtu-web-django
                        python manage.py runserver
                    ```
                }
            }
            stage('Frontend') {
                steps {
                    echo "Deploy for frontend ..."
                    bat ```
                        cd client
                        npm run dev
                    ```
                }
            }
        }
    }

    post {
        always {
                echo "Pipiline finished"
            }
            success {
                echo "Pipiline success"
            }
            failure {
                echo "Pipiline failure"
            }
            aborted {
                echo "Pipeline aborted"
            }
    }
}