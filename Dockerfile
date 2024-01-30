FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.11.7-slim as base
WORKDIR /usr/app


COPY . .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir -r requirements.txt

FROM --platform=linux/amd64 public.ecr.aws/sam/build-python3.11:latest


EXPOSE 8000/tcp
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
