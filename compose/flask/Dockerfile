FROM python:3


RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN mkdir /app
COPY  requirements.txt /app/requirements.txt

# RUN python3 -m pip install -r /app/requirements.txt

COPY ./ ./app
WORKDIR /app
RUN  pip install -r requirements.txt

EXPOSE 5000
CMD ["python3", "main.py"]