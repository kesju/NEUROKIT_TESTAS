FROM python@sha256:4fd903851bddfd9738eef5421a7775f11ee6d49f05f6f6c77be4634560f97e04

RUN mkdir /source
WORKDIR /source

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY rpeaks_sulyginimas.py ./

CMD ["/bin/bash"] 
