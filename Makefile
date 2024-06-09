# Change these if you restructure your project
SRC_DIR := src
TESTS_DIR := tests
REQUIREMENTS_FILE := requirements.txt
DOCKER_IMAGE_NAME := myapp

# Targets (I believe they're self explanatory enough)
run:
	uvicorn $(SRC_DIR).main:app --reload

test:
	python $(TESTS_DIR)/test_api.py

pull:
	git pull

push:
	@call gitpush.bat

install:
	pip install -r $(REQUIREMENTS_FILE)

clean:
	rm -rf __pycache__ .pytest_cache

docker-build:
	docker build -t $(DOCKER_IMAGE_NAME) .

docker-run:
	docker run -p 8000:8000 $(DOCKER_IMAGE_NAME)
