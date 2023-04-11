FROM python:2.7-
WORKDIR /worker
ADD . /api
RUN pip install -r requirements.txt
CMD ["python", "api.py"]
