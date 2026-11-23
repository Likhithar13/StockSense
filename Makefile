.PHONY: install run test seed
install:
	python -m pip install -r requirements.txt
run:
	python -c "from app import app,db; app.app_context().push(); db.create_all()" && flask --app app run --debug
seed:
	flask --app app seed
test:
	pytest --cov=app --cov=services --cov-report=term-missing
