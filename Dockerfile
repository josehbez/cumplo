FROM python:3.6-alpine

RUN apk update && apk add vim bash
RUN apk add --virtual build-deps gcc python3-dev musl-dev \
&& apk add --no-cache mariadb-dev

ENV DIR_DJ=/opt/django
RUN mkdir -p ${DIR_DJ}
WORKDIR ${DIR_DJ}
COPY . .
RUN pip install -r requirements.txt
RUN apk del build-deps

EXPOSE 8000
ENTRYPOINT ["bash"]

CMD [ "entrypoint.sh" ]
