FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
RUN pip install install bson
RUN pip install install pymongo
EXPOSE 80



CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]