FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Install uv (pinned version for reproducibility)
RUN curl -LsSf https://astral.sh/uv/0.9.8/install.sh | sh

# Add uv and .venv to PATH for vscode user
ENV PATH="/home/vscode/.cargo/bin:/workspaces/funding-tracker/.venv/bin:$PATH"

# Switch to vscode user
USER vscode

# Set working directory
WORKDIR /workspaces/funding-tracker
