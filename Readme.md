# Wine price analyst

The project aims the analysis of the changes in the price of wines in widely known European wine regions,
based on publicly available data.

## Implementation
A microservice-based software architecture with the following components:
- PostreSQL database
- Data collector service
- Data processor service
- Frontend
- RabbitMQ message broker

## Data source
API documentation:

https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html

Ingestion endpoint:

https://ec.europa.eu/agrifood/api/wine/prices

## Service description
The collector service fetches data from the API and stores it in the database. It produces a message for the processor service whenever a new batch of data is available.

The processor service aggregates and processes the raw data from the data collector service. It calculates the average price of wines for each country and stores the results in the database.

The frontend provides a user interface for visualizing and exploring wine price data. It allows users to select a country and view the average price of wines over time. The data is fetched from the data processor service, which aggregates and processes the raw data from the data collector service. The frontend uses Vue.js and Chart.js for data visualization.

## Deployment (in Docker)
You can deploy the project using Docker Compose.

To start the project, run the following command in the project root directory:
```bash
docker-compose up
```
This will start all the services defined in the `docker-compose.yml` file.
