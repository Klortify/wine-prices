# Wine price analyst

The project aims the analysis of the changes in the price of wines in widely known European wine regions.

## Implementation
A microservice-based software architecture with the following components:
- PostreSQL database
- Data collector service
- Data processor service
- Data publisher service
- RabbitMQ message broker

## Data source
API documentation:

https://agridata.ec.europa.eu/extensions/DataPortal/API_Documentation.html

Ingestion endpoint:

https://ec.europa.eu/agrifood/api/wine/prices