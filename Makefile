test:
	python -m unittest discover -s tests/

zip:
	(PROJECT=$(notdir $(shell pwd)) && rm -vf ../$${PROJECT}.zip && 7z a -tzip ../$${PROJECT}.zip . '-x!.venv' '-x!.idea' -r '-x!__pycache__' '-x!*.pyc')

#setup:
#	python3 -m venv .venv
#	. .venv/bin/activate
#	pip install -r requirements.txt

