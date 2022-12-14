# Airflow on Azure

This repo contains instructions, samples,and best practices for using Apache Airflow on Azure

## Pre-requisite

- Python 2 or 3
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [psql](https://www.postgresql.org/docs/10/app-psql.html)

## Getting Started

- Using Azure CLI:
  - Create service principal
    - Run `az ad sp create-for-rbac --skip-assignment` and note `appId` and `password`

- In `./terraform`:
  - Replace the default for `aks_sp_client_id` and `aks_sp_client_secret` with the generated service principal `appId` and `password` respectively
  - Run `terraform plan -out=out.tfplan`
  - Run `terraform apply out.tfplan`. This process may take up to 5 hours (Azure Redis takes a long time to provision)

- In `./docker`:
  - Run `docker build --rm -t <azure-container-reg-login-server>/docker-airflow .` to build airflow docker image
  - Run `az acr login --name <azure-container-reg-name>` to login to container registry
    - For more authentication methods, please see [this](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-authentication)
  - Run `docker push <azure-container-reg-login-server>/docker-airflow` to push airflow docker images to ACR

- Through Portal:
  - Allow connection from your client to APG
    - Navigate to "azure-airflow-pgsrv" -> Select "Connection Security" -> Click "Add Client IP" -> Click "Save"

- In `./`:
  - Create `airflow` database user and grant it access to `airflow` database
    - Run `psql -h <pg-server-name>.postgres.database.azure.com -U <pg-username>@<pg-server-name> -d airflow -c "create user airflow with encrypted password 'foo'; grant all privileges on database airflow to airflow;"`

- In `./helm`:
  - Generate fernet key for Airflow (instructions [here](https://bcb.github.io/airflow/fernet-key))
  - In `airflow.yaml`, place the generated fernet key as the value of `fernetKey`
  - In `airflow.yaml`, place `postgresql+psycopg2://airflow@<pg-server-name>:foo@<pg-server-name>.postgres.database.azure.com:5432/airflow?sslmode=require` as the value of `sqlalchemy_connection`

- Configure `kubectl` to use AKS cluster context:
  - Run `az aks get-credentials --name <airflow-aks-resource-name> --resource-group <airflow-resource-group-name>`
    - After context has been merged locally, run `kubectl config use-context <airflow-aks-resource-name>` subsequently

## References

- https://azure.microsoft.com/en-us/blog/deploying-apache-airflow-in-azure-to-build-and-run-data-pipelines/
  - https://github.com/Azure/azure-quickstart-templates/tree/master/101-webapp-linux-airflow-postgresql/
- https://medium.com/analytics-and-data/setting-up-airflow-on-azure-connecting-to-ms-sql-server-8c06784a7e2b
- (extra: Databricks & Airflow) https://docs.azuredatabricks.net/user-guide/dev-tools/data-pipelines.html
- https://blog.godatadriven.com/airflow-on-aks
- https://gtoonstra.github.io/etl-with-airflow/deployments.html
- https://github.com/PowerDataHub/terraform-aws-airflow

## Next Steps

- [] Implement [celery executor](https://airflow.apache.org/_api/airflow/executors/celery_executor/index.html)
- [] Implement [kubernetes executor](https://airflow.readthedocs.io/en/stable/kubernetes.html)