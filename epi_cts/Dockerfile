# 'celery' Docker image is Python 3.5 based!
FROM celery:3

# Install Python Dependencies
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

# Copy the project code
COPY . /src/
WORKDIR /src

ENTRYPOINT ["celery worker -A tasks -Q epi -l info -n epi_worker -c 2"]