

help: 
		@echo " airflow-build:     		Builds the docker images from the docker-compose file"
		@echo " airflow-start:     		Starts the containers created from the docker-compose file"
		@echo " airflow-up:				Creates and starts containers for airflow"
		@echo " airflow-stop:			Stops containers created from the docker-compose file"
		@echo " airflow-down:			Removes containers created by build/start-run command"
		@echo " init-terraform:			Initializes terraform configuration"
		@echo " apply-terraform:		Builds the Azure Cloud infra using terraform"
		@echo " destroy-infra:			Destroys the Azure Cloud infra created using terraform"
		@echo " terraform-config:		Creates the configuration.env file from terraform output.tf file"
		

init-terraform:
		cd ./terraform && terraform init
apply-terraform:
		cd ./terraform && terraform apply
terraform-config:
		cd ./terraform && terraform output > ../airflow/tasks/configuration.env
destroy-infra:
		cd ./terraform && terraform destroy
airflow-build:
		docker-compose build
airflow-start:
		docker-compose start
airflow-up:
		docker-compose up -d
airflow-stop:
		docker-compose stop
airflow-down:
		docker-compose down