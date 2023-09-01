# Build the application within Docker Container
build: 
	docker-compose build

# Run the application within Docker Container along with build
start: 
	docker-compose up --build

# Stop the application within Docker Container
stop: 
	docker-compose down

# Clean the application within Docker Container
clean: 
	docker-compose down --rmi all --volumes --remove-orphans

# Run the tests within Docker Container
run_tests: 
# Start the docker containers
	docker-compose up --build
# Run tests
	docker-compose exec -T app bash /scripts/test/exec-tests.sh "$@"
	docker-compose exec -T core bash /scripts/test/exec-tests.sh "$@"
