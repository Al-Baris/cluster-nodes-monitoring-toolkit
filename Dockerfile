FROM python:3.12.3

WORKDIR /cxs
ENV TZ=Europe/Berlin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV CXS_CORE https://10.1.1.000
ENV CXS_CORE_PORT 9000
ENV CXS_CORE_USERNAME username
ENV CXS_CORE_PASSWORD password

COPY cxs_monitoring_cluster.py .
COPY cxs_monitoring_nodes.py .
COPY main.py .

CMD ["python", "main.py"]
