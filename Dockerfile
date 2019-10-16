FROM python

EXPOSE 8080



RUN mkdir /code
COPY . /code/
WORKDIR /code/code


RUN pip install --upgrade pip
RUN pip3 install git+https://github.com/rthalley/dnspython
RUN pip3 install easyzone
RUN pip3 install pyyaml


CMD ["python","migrate.py"]
