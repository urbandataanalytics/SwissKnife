FROM python:3.6.9-alpine

## extra dependencies
RUN apk update && apk add gcc musl-dev

RUN mkdir project/ && cd project

WORKDIR /project

# Copy the relevant files (some will be ignored thanks to .dockerignore)
COPY SwissKnife/ ./SwissKnife
COPY tests/ ./tests
COPY setup.py .
COPY docker/entrypoint.sh .
COPY README.md .

# Install all dependencies and the package itself
RUN pip install ".[all]"

# Our entrypoint is the script launcher.sh
ENTRYPOINT ["sh", "entrypoint.sh"]