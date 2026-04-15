FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Add the venv to the PATH so 'python' automatically uses the uv environment
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /bin/

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --python 3.12

# Copy project
COPY . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Expose both Django (8000) and Debugger (5678) ports
EXPOSE 8000 5678

# Updated CMD to launch via debugpy
CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "lesson_scheduler_api/manage.py", "runserver", "0.0.0.0:8000", "--nothreading", "--noreload"]