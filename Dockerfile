FROM python:3.13
ADD . .
RUN pip install -r requirements.txt
CMD ["python3", "./app.py"]