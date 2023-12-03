build-wheel:
	python setup.py bdist_wheel

format:
	black .

lint:
	pylint --rcfile=.pylintrc tab2dict

test:
	pytest -s

test-cov:
	pytest -s --cov

