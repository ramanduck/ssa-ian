# SSA - Carlos (20th Feb 2024)

### Setup Docker
https://docs.docker.com/desktop/ </br>
https://docs.docker.com/compose/install/

### Copy the environment file and enter the values to be used:
```
cd setup
cp .env.example .env
```

### Run the docker images
```
docker-compose up --build
``` 

## Problem Statement
At Mindtickle, a client has requested a custom report that lists all active users on the platform and the number of daily lessons they have completed in the last 30 days. Your task is to create a Python script to generate this report and save it in an AWS S3 Bucket.

The data for this report is spread across two different databases: PostgreSQL and MySQL. You are not required to create the database, but you have access to the docker-compose file which will create the sample databases for you.

Criteria:
1. Understanding of the problem.
2. Correctness and efficiency of the solution
3. Clarity of the code written.

**Note:**
- Follow all the best practices you would follow for a production grade code.
