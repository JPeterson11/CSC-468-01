FROM python:2.7-
WORKDIR /worker
ADD . /worker
RUN pip install -r requirements.txt
CMD ["python", "worker.py"]
