all: down up-and-regen-creds

down:
	docker-compose down

up-and-regen-creds: generate_creds up

up: down build
	docker-compose up -d
	docker-compose logs -f

build:
	docker-compose build

generate_creds:
	./generate_password_and_set_passwords.sh
