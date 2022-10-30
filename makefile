# commands
.PHONY: run
run:
	@echo "Building and running application" && \
	docker-compose down --remove-orphans && \
	docker-compose up --build -d

.PHONY: attach
attach:
	@echo "Attaching to containers" && \
	docker exec -it training-app sh

ARG=""
.PHONY: test
test:
	@echo "Running Testing" && \
	docker exec -it training-app sh -c "pytest $(ARG)"

.PHONY: tox
tox:
	@echo "Running tox" && \
	docker exec -it training-app sh -c "tox"

.PHONY: deploy
deploy:
	@echo "Deploying application" && \
	ansible-playbook ansible/deploy.yml -i ansible/hosts -K

.PHONY: generate-key
generate-key:
	@echo 'generating-key' && \
	python -q run python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
