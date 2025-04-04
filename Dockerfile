FROM python:3.13.2-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY build build

ENTRYPOINT [ "python", "build/build.py" ]
