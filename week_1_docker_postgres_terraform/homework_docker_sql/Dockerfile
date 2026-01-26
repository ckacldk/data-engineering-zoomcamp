FROM python:3.13
ENTRYPOINT ["bash"]

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/