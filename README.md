# Lutron Permit Capstone

## Run Ingestion Scripts
- Run all scripts: `./run.sh --ingest`
- Run a specific script: `./run.sh --ingest <get/strip/combine>`

## Run Unit Tests
- Test strip script: `./run.sh --test strip`
- Test combine script: `./run.sh --test combine`

## Dependencies
- Install dependencies: `./run.sh --install`
- Save dependencies: `./run.sh --reqs`

## Delete Data Directory
`./run.sh --clean`


## NOTE: All AWS Lambda functions must be compiled on a Linux-Machine (Either Docker or machine) to be deployed properly ##
## Run Docker File  
- Build docker: `docker build -t lutron .`
- Run docker: `docker run --privileged --rm -v /c/Users/Wilso/Desktop/lutron:/root --name lutrondev -it lutron`

## Get Lambda get_data_deploy zip file to deploy to AWS
- `docker cp lutrondev:get_data_deploy.zip C:\Users\Wilso\Desktop\lutron\Lutron-PermitDataAnalytics`
## Afterwards drag get_data_deploy.zip folder into s3 bucket and refer to the s3 URI to call lambda function.
## Handler for get_data socrata get_data_socrata.lambda_handler
## Handler for get_data non_socrata: get_data_non_socrata.lambda_handler

### Contributors ###

* Kunj S.
* Ayon B.
* Bharath J.
* Wilson Z.
