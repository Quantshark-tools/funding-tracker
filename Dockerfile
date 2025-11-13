FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Install git for dependencies from GitHub
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy dependency files and README (required for package metadata)
COPY pyproject.toml uv.lock README.md ./

# Copy application code
COPY . .

# Install dependencies
RUN uv sync --frozen --no-dev

# Add venv to PATH so we can call scripts directly
ENV PATH="/app/.venv/bin:$PATH"

# Copy and set entrypoint
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]