FROM python:3.9-slim
WORKDIR /usr/src/bookingapp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src/bookingapp.py .
CMD ["python", "./bookingapp.py"]