clean:
	@find . -name "*.pyc" -delete

upload:
	@python setup.py sdist upload
