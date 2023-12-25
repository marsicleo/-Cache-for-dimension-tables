
FROM python:3.10.12

WORKDIR /eksperimental

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 2>&1 | tee pip-install.log


COPY . .

CMD ["python", "main.py"]
