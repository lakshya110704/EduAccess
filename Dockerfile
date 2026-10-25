FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencies first so this layer is cached until requirements.txt changes.
COPY requirements.txt .
RUN pip install --require-hashes -r requirements.txt

COPY . .

# Bake static files into the image. collectstatic needs settings to load but never touches the
# database or uses the secret key for anything, so a throwaway value is fine here.
RUN DJANGO_SECRET_KEY=collectstatic-only DJANGO_DEBUG=False python manage.py collectstatic --noinput

# gunicorn writes its control socket under the user's home directory, so the user needs one.
RUN useradd --system --uid 10001 --create-home app
USER app

EXPOSE 8000
ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["gunicorn", "eduaccess_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
