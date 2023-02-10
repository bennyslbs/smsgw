#-*-conf-*-

FROM python:3

WORKDIR /usr/src
VOLUME /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY smsgwd.cfg /etc/.

CMD [ "python", "app/smsgwd"]
