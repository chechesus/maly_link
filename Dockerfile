FROM python:bullseye
RUN pip install redis
COPY . /src
WORKDIR /src
ENTRYPOINT ["python", "api.py"]
EXPOSE 8000
