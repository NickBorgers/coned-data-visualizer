all: down up

down:
	docker-compose down

up: down build generate_creds
	docker-compose up -d

build:
	docker-compose build

generate_creds:
	./generate_password_and_set_passwords.sh