pipeline {
    agent any

    stages {
        stage("cloning from github..."){
            steps{
                script{
                    echo "cloning from github..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'kidney-github-token', url: 'https://github.com/htasoftware99/kidney_disease_mlops.git']])
                }
            }
        }
    }
}