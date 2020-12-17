FROM python:3.7.3-stretch

RUN mkdir /app
WORKDIR /app

COPY . . 

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]