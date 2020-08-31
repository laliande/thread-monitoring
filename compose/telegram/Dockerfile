FROM python:3


RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN mkdir /app
COPY  requirements.txt /app/requirements.txt

# RUN python3 -m pip install -r /app/requirements.txt

COPY ./ ./app
WORKDIR /app
RUN  pip3 install -r requirements.txt

EXPOSE 5000
CMD ["python3", "run-bot.py"]