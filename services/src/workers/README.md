# Serverless Worker Functions
This folder contains the worker code used to perfrom CRUDs on vector DBs and/or DB. These endpoints are triggered by events from SQS and pushing to SNS and are responsible for processing the data and storing it in the vector databases, as well as 
updating the ticket status in the main database.