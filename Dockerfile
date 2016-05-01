FROM mattmcd/pcr 

MAINTAINER Matt McDonnell "matt@matt-mcdonnell.com"

ENV MDA_DATA_DIR /home/ubuntu/Work/Data

RUN mkdir -p /home/ubuntu/Work

WORKDIR /home/ubuntu/Work

COPY . /home/ubuntu/Work/PyAnalysis

CMD ["python", "/home/ubuntu/Work/PyAnalysis/download_intraday.py", "--do-copy"]

