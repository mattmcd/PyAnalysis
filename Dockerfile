FROM continuumio/miniconda

MAINTAINER Matt McDonnell "matt@matt-mcdonnell.com"

RUN conda install pandas

RUN pip install tqdm

RUN pip install boto3

RUN conda install fabric

ENV MDA_DATA_DIR /home/ubuntu/Work/Data

RUN mkdir -p /home/ubuntu/Work

WORKDIR /home/ubuntu/Work

COPY . /home/ubuntu/Work/PyAnalysis

CMD ["python", "/home/ubuntu/Work/PyAnalysis/download_intraday.py"]

