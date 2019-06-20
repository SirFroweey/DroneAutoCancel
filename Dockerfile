# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV WEBHOOK_VERIFY_TOKEN test
ENV DRONE_SERVER https://drone.britecorepro.com
ENV DRONE_TOKEN 6sg2A5TiXwJ79k50Fm7DVtRfEnbotkIt
ENV DRONE_REPO_OWNER_USERNAME SirFroweey
ENV DRONE_REPO_NAME BriteCore
ENV ONLY_PROCESS_PR_EVENTS True

CMD ["python", "run.py"]