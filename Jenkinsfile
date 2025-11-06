pipeline {
    agent any    
    
    stages {
        stage('Build') {
            parallel {
                stage('Backend') {
                    steps {
                        echo "Build for backend ..."
                        bat '''
                            cd backend
                            conda env create -f environment.yml                                                        
                            conda run -n inrtu-web-django python manage.py makemigrations
                            conda run -n inrtu-web-django python manage.py migrate
                        '''
                    }
                }
                stage('Frontend') {
                    steps {
                        echo "Build for frontend ..."
                        bat '''
                            cd frontend
                            npm i                                           
                        '''
                    }
                }
            }
        }
        stage('Test') {
            steps {
                echo "Running tests ..."
                bat '''
                    cd backend
                    conda run -n inrtu-web-django python manage.py test characters.tests'''
            }
        }
        stage('Deploy') {
            when { 
                branch = 'main'
            }
            parallel {
                stage('Backend') {
                    steps {
                        echo "Deploy for backend ..."
                        echo 'Backend started'
                        // bat '''
                        //  conda run -n inrtu-web-django python manage.py runserver
                        // 
                        // '''
                    }
                }
                stage('Frontend') {
                    steps {
                        echo "Deploy for frontend ..."
                        echo 'Fronted started'
                        // bat '''
                        //     cd frontend
                        //     npm run dev
                        // '''
                    }
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