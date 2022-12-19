# Overview
Real Estate Market Analyzer is a proof-of-concept project that demonstrates a set of *Big Data Technologies* and how to use them. 

In general, this project focuses on collecting data from Switzerland's largest real estate marketplace (aka homegate.ch), storing it in Microsoft Azure, and finally displaying it in PowerBI. Furthermore, these data are accessible via an API, from which any app can retrieve data and initiate new searches.

# Architecture

The tools and technologies that have been utilized in this project are:

- **Python** as the main programming language.
- **Airflow** as an orchestration tool to schedule the scraping jobs.
- **Docker** as a multicontainer infrastructure (Docker Compose) for hosting the Airflow instance.
- **Pydantic** as a data validation library to verify the scraped data.
- **Flask** in order to create an API that serves http requests.
- **Terraform** as a tool for infrastructure management.
- **PowerBI** as a data visualization tool.