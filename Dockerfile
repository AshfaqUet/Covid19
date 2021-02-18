FROM python:3.6

ADD . /Covid19
WORKDIR /Covid19

RUN pip install -r requirements.txt
ENV FLASK_APP='manage.py'
RUN export FLASK_APP='manage.py'
CMD ["flask", "run","--host=0.0.0.0","--port=5000"]
