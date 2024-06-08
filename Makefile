run:
	uvicorn src.main:app --reload

test:
	python tests/test_api.py

pull:
	git pull

push:
	@call gitpush.bat