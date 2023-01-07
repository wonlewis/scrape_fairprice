# As Scrapy runs on Python, I choose the official Python 3 Docker image.
FROM python:3.9

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install VIM
RUN apt-get update && apt-get install apt-file -y && apt-file update && apt-get install vim -y

# Set timezone for image
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Singapore /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
ENV TZ="Asia/Singapore"

# Install Scrapy specified in requirements.txt.
RUN pip install --upgrade pip setuptools wheel
RUN pip install \
    scrapy \
    apscheduler \
    pg8000 \
    python-dotenv

# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .

# Run the crawler when the container launches.
CMD [ "python3", "./scroll_fp/main.py" ]