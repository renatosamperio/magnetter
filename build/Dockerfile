ARG REGISTER=docker.io
ARG VERSION=3.9.20
ARG SUFFIX=-bullseye

FROM ${REGISTER}/python:${VERSION}${SUFFIX}

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        curl \
        git \
        wget

COPY ./build/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Copy the requirements file and app files to the container
COPY src /opt/magnetter

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the Flask app
WORKDIR /opt/magnetter
CMD ["python", "app.py"]