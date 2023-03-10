# Subsector Interface

The Subsector Interface can be deployed as an dockerized container in an EC2 instance (preferably in an `t2.small` instance).

After the ssh login to the EC2 instance, there we need to install `docker` and `docker-compose` (Follow one of the tutorials from the web)

Then, we need to configure the `.env` file which contains details about establishing connection to the database (assume we already setup a db in AWS RDS)

Then, we can run the build the image and run the container.
>$ docker-compose up -d --build

Then, we can access the container using following command:
>$ docker-compose exec -it -u root <container-id> /bin/bash

Then, run the script `db_orm.py` to create the database and respective tables.
>$ python db_orm.py

Some configurations need to done at the Route 53 for DNS (contact admin)

The subsector interface should be available at `https://sectortagging.labs.thedeep.io`