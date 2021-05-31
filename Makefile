ENV=local
include ./secrets/$(ENV)/.env
S3_BUCKET=boilerplate
APP_NAME=boilerplate

ifeq ($(ENV), prod)
	DOMAIN=$(BASE_DOMAIN)
else
	DOMAIN=$(ENV).$(BASE_DOMAIN)
endif

push_secrets:
	aws s3 cp ./secrets/$(ENV)/.env s3://$(S3_BUCKET)/$(APP_NAME)/backend/$(ENV)/.env

pull_secrets:
	aws s3 cp s3://$(S3_BUCKET)/$(APP_NAME)/backend/$(ENV)/.env ./secrets/$(ENV)/.env

use_secrets: pull_secrets
	cp ./secrets/$(ENV)/.env ./.

down:
	docker-compose down

build: use_secrets
	docker-compose build

up: build
	docker-compose up -d

unit_tests: up
	docker-compose exec -T backend pytest -s --cov-report term-missing --cov=. ./tests/unit/

some_unit_tests: up
	docker-compose exec -T backend pytest -s --cov-report term-missing --cov=. ./tests/unit/$(TEST_PATH)

integration_tests: up
	docker-compose exec -T backend pytest -s --cov-report term-missing --cov=. ./tests/integration/

some_integration_tests: up
	docker-compose exec -T backend pytest -s ./tests/integration/$(TEST_PATH)

build_backup:
	docker build -f backup.Dockerfile --tag backup:latest --build-arg AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) --build-arg AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) --build-arg AWS_REGION=$(AWS_REGION) --build-arg S3_BUCKET_BACKUP_NAME=$(S3_BUCKET_BACKUP_NAME) --build-arg MONGO_USERNAME=$(MONGO_USERNAME) --build-arg MONGO_PASSWORD=$(MONGO_PASSWORD) --build-arg MONGO_HOST=$(MONGO_HOST) --build-arg MONGO_PORT=$(MONGO_PORT) --build-arg MONGO_NAME=$(MONGO_NAME) --build-arg BACKUP_LIFETIME_DAYS=$(BACKUP_LIFETIME_DAYS) .

backup:
	docker run --network backend backup:latest python backup.py

tests: up
	docker-compose exec -T backend pytest -s --cov-report term-missing --cov=. ./tests/

tag: build
	docker tag $(APP_NAME):latest $(APP_NAME):$(ENV)

deploy: tag
	docker save --output ./deploy/files/app $(APP_NAME):latest
	docker save --output ./deploy/files/background $(APP_NAME)_background:latest
	ansible-playbook -i deploy/inventory/$(ENV) deploy/tasks/deploy.yml --extra-vars "server_username=$(SERVER_USERNAME) domain=$(DOMAIN) slack_token=$(SLACK_TOKEN)"
	rm ./deploy/files/app
	rm ./deploy/files/background

deploy_backup:
	docker save --output ./deploy/files/backup backup:latest
	ansible-playbook -i deploy/inventory/$(ENV) deploy/tasks/setup_backups.yml --extra-vars "server_username=$(SERVER_USERNAME)"
	rm ./deploy/files/backup

setup_infrastructure:
	ansible-playbook -i deploy/inventory/$(ENV) deploy/tasks/setup_infrastructure.yml --extra-vars "email=$(EMAIL) server_username=$(SERVER_USERNAME) domain=$(DOMAIN)"

boilerplate_tests: boilerplate_up
	docker-compose exec -T backend pytest -s --cov-report term-missing --cov=. ./tests/

boilerplate_up: boilerplate_build
	docker-compose up -d

boilerplate_build:
	docker-compose build
