reqs:
	pip install pipreqs
	pipreqs . --force

install:
	pip install -r requirements.txt

ingest:
	cd ingestion
	if [ ! -d "raw_data" ]; then mkdir raw_data; fi
	if [ ! -d "stripped_data"]; then mkdir stripped_data; fi
	if [ ! -d "combined_data"]; then mkdir combined_data; fi
	python get_socrata_data.py
	python get_data.py
	python strip_data.py
	python combine_data.py
