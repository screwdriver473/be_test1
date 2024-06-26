FROM python:3.12

ARG docker_backend_root_dir="backend"

# Set global trusted hosts for pip
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"

WORKDIR /${docker_backend_root_dir}

# Copy your application code into the container
COPY . .

# Copy your requirements.txt file into the container
#COPY ./requirements.txt /${docker_backend_root_dir}/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Setup the environment and postgre DB
RUN ./docker_backend_prep.sh

WORKDIR /${docker_backend_root_dir}/app
#RUN /bin/echo "3" >> /log
#RUN pwd >> /log

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--port", "5438" ]