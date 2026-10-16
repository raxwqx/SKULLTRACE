.PHONY: test check install

install:
	python3 -m pip install -e .

test:
	python3 -m unittest discover -s tests -v

check:
	python3 -m compileall -q src tests
	python3 -m unittest discover -s tests -v
