FROM python:3.9.7
ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
RUN pip uninstall -y PyJWT
RUN pip install PyJWT
# RUN python manage.py migrate
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "GreenCity.wsgi", "--log-file", "-"]
