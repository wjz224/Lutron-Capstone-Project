reqs:
	pip install pipreqs
	pipreqs . --force

install:
	pip install -r requirements.txt

ingest:
	cd ingestion
	python get_socrata_data.py
	
