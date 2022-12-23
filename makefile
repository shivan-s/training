# commands
.PHONY: run-detached
run-detached:
	@echo "Building and running application detached" && \
	docker-compose down --remove-orphans && \
	docker-compose -build --wait

.PHONY: run
run:
	@echo "Building and running application" && \
	docker-compose down --remove-orphans && \
	docker-compose up --build

.PHONY: attach
attach:
	@echo "Attaching to containers" && \
	docker exec -it trainwithsomeone_web sh

.PHONY: tail
tail:
	@echo "Attaching to debug.log" && \
	docker exec -it trainwithsomeone_web sh -c "tail -f debug.log"

.PHONY: shell
shell:
	@echo "Attaching to django shell" && \
	docker exec -it trainwithsomeone_web sh -c "python manage.py shell_plus"

ARG=""
.PHONY: test
test:
	@echo "Running Testing" && \
	docker exec -it trainwithsomeone_web sh -c "pytest $(ARG)"

.PHONY: tox
tox:
	@echo "Running tox" && \
	docker exec -it trainwithsomeone_web sh -c "tox"

.PHONY: generate-key
generate-key:
	@echo 'generating-key' && \
	python -q run python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

.PHONY: graph
graph:
	@echo "Generating graph viz of database"
	docker exec -it trainwithsomeone_web  sh -c "python manage.py graph_models --rankdir BT project users -o ./docs/my_project_visualised.png" && \
	exit
	open ./docs/my_project_visualised.png

.PHONY: debug
debug:
	@echo "Debugging..." && \
	docker exec -it trainwithsomeone_web sh -c "tail -f debug.log"
