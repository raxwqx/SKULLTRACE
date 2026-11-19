.PHONY: test check install

install:
	python3 -m pip install -e .

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

check:
	PYTHONPATH=src python3 -m compileall -q src tests
	PYTHONPATH=src python3 -m unittest discover -s tests -v
