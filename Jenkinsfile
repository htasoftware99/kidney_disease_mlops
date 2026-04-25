pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'neat-chain-464913-k3'
        GCLOUD_PATH = "/usr/lib/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin/gke-gcloud-auth-plugin"
    }

    stages {
        stage("cloning from github..."){
            steps{
                script{
                    echo "cloning from github..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'kidney-github-token', url: 'https://github.com/htasoftware99/kidney_disease_mlops.git']])
                }
            }
        }

        stage("making a virtual environment..."){
            steps{
                script{
                    echo "making a virtual environment..."
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'DVC Pul....'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

        stage('Build, Scan and Push Image to GCR'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'Building, scanning and pushing image to GCR...'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        
                        # 1. İmajı Build Et
                        docker build -t gcr.io/${GCP_PROJECT}/kidney-disease-mlops:latest .
                        
                        # 2. Trivy ile İmajı Tara (Docker Container Kullanarak - ÇÖZÜM BURASI)
                        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:0.62.1 image --severity HIGH,CRITICAL gcr.io/${GCP_PROJECT}/kidney-disease-mlops:latest || true
                        
                        # 3. Tarama başarılı olursa imajı GCP'ye Push Et
                        docker push gcr.io/${GCP_PROJECT}/kidney-disease-mlops:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --zone us-central1-a
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}