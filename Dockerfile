FROM alpine:latest
EXPOSE 9000
COPY requirements.txt gunicorn_config.py /tmp
RUN apk add python3 python3-dev py3-pip git
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app
RUN git clone https://github.com/collin-clark/password-generator.git .

CMD ["gunicorn","--config", "/tmp/gunicorn_config.py", "app:app"]
