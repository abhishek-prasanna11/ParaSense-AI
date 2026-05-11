FROM python:3.10-slim

WORKDIR /app

# Dynamic installation based on CPU architecture
ARG TARGETARCH
RUN if [ "$TARGETARCH" = "amd64" ]; then \
      pip install --no-cache-dir torch==2.4.1+cpu torchvision==0.19.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu; \
    else \
      pip install --no-cache-dir torch==2.4.1 torchvision==0.19.1; \
    fi

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
