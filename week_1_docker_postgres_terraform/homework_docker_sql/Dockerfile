#FROM python:3.13
#ENTRYPOINT ["bash"]

FROM python:3.13.11
# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

RUN pip install pandas pyarrow

WORKDIR /code

#Copy these files to the docker image. Can check by doing things like docker run -it --rm --entrypoint=bash test:dockertest
COPY pyproject.toml .python-version uv.lock ./
#copy the depenencies from the UV lock and from the environment. So environment is not different.
RUN uv sync --locked
COPY homework_data_pipeline.py .

ENTRYPOINT ["uv", "run", "python", "homework_data_pipeline.py"]
