reqs:
	pip install pipreqs
	pipreqs . --force

install:
	pip install -r requirements.txt

ingest:
	cd ingestion
	python get_socrata_data.py
	python get_data.py
	python strip_data.py
	python combine_data.py
