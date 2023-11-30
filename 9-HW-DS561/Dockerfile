FROM python:3.10.4-slim-bullseye

# Install Gcloud
RUN apt-get update \
    && apt-get install -y wget \
    && wget https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.tar.gz -O /tmp/google-cloud-sdk.tar.gz \
    && mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh

# Set Gcloud to the environment
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

WORKDIR /app

# Copy Source Code
COPY . /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Copy service account key file
COPY ds-561-398918-c5dc3ab0675e.json /app/ds-561-398918-c5dc3ab0675e.json

# Set the environment variable for authentication
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/ds-561-398918-c5dc3ab0675e.json

CMD [ "python3", "HW4-561.py" ]
