.DEFAULT_GOAL := help

#help: @ List available tasks on this project
help: 
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#' | sed -E 's/Makefile.//' | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#start: @ Start this up including generating elasticsearch credentials
start: down up-and-regen-creds

#down: @ Shut this down - does not delete the volumes though
down:
	docker-compose down

up-and-regen-creds: generate_es_creds up

#up: @ Build the container images and start this up, tailing the logs
up: down build
	docker-compose up -d
	docker-compose logs -f

#build: @ Just build the container images
build: 
	docker-compose build

#generate_es_creds: @ Regenerate the Elasticsearch credentials
generate_es_creds:
	./generate_password_and_set_passwords.sh

#test_coned_creds: @ Test the ConEd credentials provided in .credentials.env
test_coned_creds:
	@echo "You must create and populate a .credential.env file based on the instructions linked in the README"
	docker-compose pull
	docker-compose build
	@echo "The output will be super noisy!"
	@echo "You want to see documents get pushed to Elasticsearch!"
	@sleep 2
	timeout 90s docker-compose up coned-collector
