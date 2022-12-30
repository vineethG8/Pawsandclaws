FROM python:3.10
WORKDIR /app
ADD . /app
COPY requirement.txt /app
RUN python3 -m pip install -r requirement.txt
EXPOSE 5000
CMD ["python","app.py"]