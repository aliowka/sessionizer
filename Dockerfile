FROM python:3
ADD . /app/

ENV PYTHONPATH /app/src
ENV FLASK_APP /app/src/app.py

WORKDIR /app

EXPOSE 5000

RUN pip install -r /app/requirements.txt
RUN pytest /app/tests -v

CMD flask run --host 0.0.0.0