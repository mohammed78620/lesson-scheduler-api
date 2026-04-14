FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /bin/

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --python 3.12

# Copy project
COPY . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 8000
CMD [ "uv", "run",  "python", "lesson_scheduler_api/manage.py", "runserver", "0.0.0.0:8000"]