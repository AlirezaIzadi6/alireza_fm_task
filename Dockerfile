FROM hub.hamdocker.ir/python:3.12

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]