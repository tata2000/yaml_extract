FROM python:3.8.2-alpine as base
COPY app /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
CMD ["python3","/app/main.py"]
EXPOSE 8888

FROM base as test
COPY tests /tests



FROM base as prod






