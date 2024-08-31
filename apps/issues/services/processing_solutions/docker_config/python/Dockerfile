FROM python:3.12.4-slim

# Using python site-hooks to limit dangerous modules and funcs: https://docs.python.org/3/library/site.html
COPY restrict_python.py /usr/local/lib/python3.12/site-packages/sitecustomize.py

RUN groupadd -r sandboxuser && useradd -r -g sandboxuser sandboxuser
USER sandboxuser

WORKDIR /test_runner

# Keep the container alive
CMD ["tail", "-f", "/dev/null"]
