# Automatic Scraper of Online Supermarkets

## Purpose

This is a docker container to automatically scrape prices and items from online supermarkets. The scraping engine is powered by Scrapy, and uses Apscheduler for scheduling. The container is designed to be hosted on an instane such as AWS EC2, and the scraped data can be stored on a dedicated database such as AWS RDS postgresql.

## How to use

1.	Set up EC2 instance. A few points to note:
    a.	Take note of the accessibility zone of the EC2 instance. This must be the same as that for the RDS in order to more easily connect the EC2 with the RDS in a virtual VPC.
    b.	If you use free tier such as t2.micro with limited ram and cpu, just note that APACHE SUPERSET will not load with the examples. But that is ok, you do not really need the examples for APACHE SUPERSET to work.
    c.	Select Ubuntu as most guides using Docker assumes Ubuntu. This makes it easier to follow these guides.
2.	After the EC2 instance is set up, install Docker by following this [guide](https://docs.docker.com/engine/install/ubuntu/).
3.	Give your Docker admin rights (so that you do not have to preface all Docker commands with sudo in future) by following this [guide](https://docs.docker.com/engine/install/linux-postinstall/). Rember to log out and log in again for Docker admin access rights to take effect.
4.	Then follow this [guide](https://hub.docker.com/r/apache/superset) to install APACHE SUPERSET as a container on your EC2 instance. Note to skip step 3 on “Load Examples” if you are using t2.micro.
5.	Go to Security Group on AWS, select security group that is tied to your EC2 instance, in my case by default will be ‘launch-wizard-1’, and add a inbound rule to access the EC2 instance via port 8080 (or whichever port you have defined when setting up the APACHE SUPERSET container in step 4 above).

