# https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi

# Start from the official Python base image.
FROM python:3.12

# Set the current working directory to /code.
# This is where we'll put the requirements.txt file and the app directory.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
# Copy only the file with the requirements first, not the rest of the code.  As this file doesn't change often, Docker will detect it and use the cache for this step, enabling the cache for the next step too.
COPY ./requirements.txt ./

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the ./app directory inside the /code directory.
# As this has all the code which is what changes most frequently the Docker cache won't be used for this or any following steps easily.  So, it's important to put this near the end of the Dockerfile, to optimize the container image build times.
COPY ./src ./src

# Set the command to run the uvicorn server.
CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--reload"]
#, "--root-path", "/api"