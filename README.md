# SSA - Ian (12th Mar 2024)

## Problem Statement
At Mindtickle, a client has requested a custom report that lists all active users on the platform and the number of daily lessons they have completed in the last 1 year. Your task is to create a Python script to generate this report and save it in an AWS S3 Bucket.

The data for this report is spread across two different databases: PostgreSQL and MySQL. You are not required to create the database, but you have access to the docker-compose file which will create the sample databases for you.

Criteria:
1. Understanding of the problem.
2. Correctness and efficiency of the solution
3. Clarity of the code written.

**Note:**
- Follow all the best practices you would follow for a production grade code.


#Solution

## The application can be deployed locally as well as on AWS.

## 1. Local Deployment

### A. Setup Docker
https://docs.docker.com/desktop/ </br>
https://docs.docker.com/compose/install/

### B. Copy the environment file and enter the values to be used:
```
cd setup
cp .env.example .env
```

### C. Run the docker images to start database servers.
```
sudo docker-compose up --build -d
``` 

### D. Database servers can be stopped at any time using following commands
```
sudo docker-compose stop mt-postgres
sudo docker-compose stop mt-mysql
``` 

### E. Application runs in a docker container. Commands to build and run application container.
```
cd ../
sudo docker build -t mindtickle-assignment:0.0.1 .
sudo docker run --network setup_my_network --mount type=bind,source="$(pwd)/",target=/home/dataeng -it mindtickle-assignment:0.0.1 bash
```

### Wait for 2 minutes to let docker container finish package installation and application to load.

### F. Run following command to generate and print report.
```
poetry run main generate-report
```

### G. Run following command to generate and upload report to s3.
```
poetry run main upload-report
```

### H. Run following command to run unit tests.
```
poetry run main unit-test
```

## 2. AWS Deployment

### A. set following env variables in github secrets
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

### B. Push the code to main branch to trigger deployment job.

### C. Once the automated deployment is completed, you can trigger lambda manually or programatically.








