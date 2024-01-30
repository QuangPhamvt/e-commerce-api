FROM --platform=linux/amd64 public.ecr.aws/sam/build-python3.11:latest as base
WORKDIR /usr/app

COPY . .
RUN pip install -r requirements.txt



EXPOSE 8000/tcp
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
