clean:
	rm -f dist/*

build:
	python setup.py bdist_wheel

push:
	twine upload dist/*

pypi:   clean build push

.PHONY: clean build push pypi
