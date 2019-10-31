FROM python:3.6.9-alpine

RUN mkdir project/ && cd project

WORKDIR /project

# Copy the relevant files (some will be ignored thanks to .dockerignore)
COPY SwissKnife/ ./SwissKnife
COPY tests/ ./tests
COPY setup.py .
COPY docker/entrypoint.sh .

# Install all dependencies and the package itself
RUN python setup.py install

# Our entrypoint is the script launcher.sh
ENTRYPOINT ["sh", "entrypoint.sh"]