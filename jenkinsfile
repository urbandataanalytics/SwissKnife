pipeline {
    agent any
    stages {
        stage("Build docker image") {
            steps{
                sh 'docker build -t swissknife:latest .'
            }
        }
        stage("Do tests and verify"){
            steps{
                sh 'docker run --rm swissknife:latest > nosetests.xml'
                junit 'nosetests.xml'
            }
        }
    }
    post {
        always {
            // Clean execution
            sh "docker rmi swissknife:latest || :"
            sh "rm nosetests.xml || :"
        }
    }
}