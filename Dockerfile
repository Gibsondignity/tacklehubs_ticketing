FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput


# Install Gunicorn
RUN pip install gunicorn

# Expose the port the app runs on
EXPOSE 8000


CMD ["gunicorn", "-b", "0.0.0.0:8000", "ticketting.wsgi:application"]
