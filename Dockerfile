FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.11.7-alpine as base
WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000/tcp
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
