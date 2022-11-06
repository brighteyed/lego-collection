FROM alpine:latest

RUN apk update \ 
  && apk add --no-cache \
  git \
  curl \
  make \
  sqlite

RUN git clone https://github.com/jncraton/rebrickable-sqlite.git /rebrickable-sqlite
RUN apk del git && rm -R /rebrickable-sqlite/.git

RUN adduser -H -D --shell=/sbin/nologin bricks
RUN chown -R bricks:bricks /rebrickable-sqlite

USER bricks

CMD [ "make", "-C", "/rebrickable-sqlite" ]