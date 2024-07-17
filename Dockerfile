FROM python:3.11
ENV DockerHOME=/home/app/webapp  

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME  

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

COPY . $DockerHOME

RUN pip install --upgrade pip

RUN pip install -r req.txt

VOLUME home/app/webapp/media

EXPOSE 2001
CMD python manage.py runserver  0.0.0.0:2001
