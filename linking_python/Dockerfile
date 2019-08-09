FROM python:3.7.4-slim-stretch

WORKDIR /home
ADD requirements.txt /home/requirements.txt
ADD OntoSimPY/ /home/OntoSimPY

RUN apt-get update
RUN apt-get install -y python python-pip wget
RUN pip install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('wordnet')" ]

EXPOSE 5000

CMD ["python", "OntoSimPY/OntoSimPyMain.py" ]