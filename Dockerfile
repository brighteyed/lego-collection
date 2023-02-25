FROM python:3-alpine3.16

RUN apk update \ 
  && apk add --no-cache \
  git \
  curl \
  make \
  sqlite

RUN git clone https://github.com/jncraton/rebrickable-sqlite.git /bricks/rebrickable
RUN apk del git && rm -R /bricks/rebrickable/.git

WORKDIR /bricks/setlists

COPY requirements.txt setlists.py ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

VOLUME [ "/database" ]

CMD ["/entrypoint.sh"]
