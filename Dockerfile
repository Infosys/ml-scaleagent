
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
COPY tests ./tests
COPY startup.py ./startup.py
COPY entrypoint.sh ./entrypoint.sh

RUN pip install --no-cache-dir .
COPY tests ./tests
# Run tests during build and fail if any test fails
RUN pytest tests
RUN chmod +x /app/entrypoint.sh
ENV PYTHONPATH=/app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["api"]
