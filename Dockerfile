FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Install system dependencies 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    libssl-dev \
    pkg-config \
    cmake \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Rust 
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal --default-toolchain stable
ENV PATH="/root/.cargo/bin:$PATH"

# Upgrade pip and install Polars from source
RUN pip install --upgrade pip
RUN pip install polars==0.20.10

CMD ["python", "main.py"]
