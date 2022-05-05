FROM python:3
RUN mkdir -p /opt/hdyndns/
COPY requirements.txt /opt/hdyndns/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /opt/hdyndns/requirements.txt

COPY entrypoint.sh /opt/hdyndns/
COPY hdyndns.py /opt/hdyndns/
CMD [ "/opt/hdyndns/entrypoint.sh" ]
