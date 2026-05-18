pipeline {
    agent any
    // Added a small comment to test the Jenkins webhook trigger - run 2

    environment {
        DOCKER_USER = "abhishekprasanna1109"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/abhishek-prasanna11/ParaSense-AI.git'
            }
        }

	stage('Start Backend for Testing') {
	    steps {
		sh '''
		# Clean up any leftover container from previous runs
		docker stop test-backend 2>/dev/null || true
		docker rm test-backend 2>/dev/null || true

		docker build -t temp-backend backend/

		docker run -d -p 8000:8000 \
		  --name test-backend temp-backend

		echo "Initial logs:"
		sleep 10
		docker logs test-backend

		# Check if container crashed immediately
		if ! docker ps --format '{{.Names}}' | grep -q test-backend; then
		  echo "ERROR: Container crashed on startup!"
		  docker logs test-backend
		  exit 1
		fi

		echo "Waiting for backend to be ready (this can take up to 10 mins on first run)..."

		for i in $(seq 1 120)
		do
		  # If container died, fail fast instead of looping
		  if ! docker ps --format '{{.Names}}' | grep -q test-backend; then
		    echo "ERROR: Container stopped unexpectedly!"
		    docker logs test-backend
		    exit 1
		  fi

		  if curl -sf http://localhost:8000/docs > /dev/null
		  then
		    echo "Backend is UP"
		    break
		  fi

		  echo "Still loading... $i"
		  sleep 5
		done

		echo "Final check..."

		if ! curl -f http://localhost:8000/docs > /dev/null
		then
		  echo "Backend failed after waiting"
		  docker logs test-backend
		  exit 1
		fi
		'''
	    }
	}

        stage('Run test50') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate

                # test50.py only needs 'requests' — skip the heavy ML deps
                pip install --upgrade pip -q
                pip install requests -q

                echo "Checking backend again..."

                for i in {1..30}; do
                  if curl -sf http://localhost:8000/ >/dev/null; then
                    echo "Backend confirmed alive"
                    break
                  fi
                  sleep 2
                done

                python tests/test50.py | tee result.txt
                '''
            }
        }

        stage('Stop Test Backend') {
            steps {
                sh '''
                docker stop test-backend || true
                docker rm test-backend || true
                '''
            }
        }

        stage('Check Pass Percentage') {
            steps {
                script {
                    def percent = sh(
                        script: "grep 'Final Result' result.txt | cut -d'(' -f2 | cut -d'%' -f1",
                        returnStdout: true
                    ).trim()

                    if (!percent) {
                        error "Could not extract percentage from test output"
                    }

                    def percentage = percent.toFloat()
                    echo "Pass Percentage: ${percentage}%"

                    if (percentage < 60) {
                        error "Less than 60% passed. Stopping pipeline."
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                # Reuse the temp-backend image we already built instead of rebuilding
                docker tag temp-backend $DOCKER_USER/semantic-backend:latest
                docker build -t $DOCKER_USER/semantic-frontend:latest frontend/
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'DockerHubCred',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD'
                )]) {
                    sh '''
                    echo $PASSWORD | docker login -u $USERNAME --password-stdin

                    docker push $DOCKER_USER/semantic-backend:latest
                    docker push $DOCKER_USER/semantic-frontend:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                echo "Deploying to Kubernetes cluster..."
                kubectl apply -f k8s/
                
                # Ensure the latest image is pulled by restarting the deployments
                kubectl rollout restart deployment semantic-backend
                kubectl rollout restart deployment semantic-frontend
                '''
            }
        }

        stage('Deploy ELK Monitoring') {
            steps {
                sh '''
                echo "Deploying ELK Monitoring Stack..."
                kubectl apply -f k8s/monitoring/

                echo "Waiting for Elasticsearch to be ready..."
                kubectl rollout status deployment/elasticsearch --timeout=180s || true
                kubectl rollout status deployment/logstash --timeout=120s || true
                kubectl rollout status deployment/kibana --timeout=120s || true

                echo "ELK Monitoring Stack deployed."
                echo "Kibana will be available on NodePort 30601"
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker stop test-backend || true
            docker rm test-backend || true
            '''
        }
    }
}
