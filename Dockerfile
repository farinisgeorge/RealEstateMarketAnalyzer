

FROM --platform=linux/amd64 apache/airflow:2.4.2
USER root

# The next lines will download de odbc driver required for connecting to Azure Synapse
# Updates packages list for the image
RUN apt-get update

# Installs transport HTTPS
RUN apt-get install -y curl apt-transport-https

# Retrieves packages from Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Updates packages for the image
RUN apt-get update

# Installs SQL drivers and tools
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Installs MS SQL Tools
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools



RUN apt-get install -y gosu\
    && apt-get install -y gcc \
    && apt-get clean \
    # This line will install the Azure CLI inside the Airflow Containers
    && curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash



USER airflow
# These are the dependencies for the code. It can also be done using a requirements.txt file
# or a Piplock file
RUN pip3 install --no-cache-dir beautifulsoup4
RUN pip3 install --no-cache-dir requests-html
RUN pip3 install --no-cache-dir pydantic
RUN pip3 install --no-cache-dir python-dotenv
RUN pip3 install --no-cache-dir pyodbc
RUN pip3 install --no-cache-dir sqlalchemy


RUN mkdir /opt/airflow/dags/files
COPY api /opt/airflow/dags/files