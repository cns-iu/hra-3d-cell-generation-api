FROM node:20-bookworm AS build
ARG DEBIAN_FRONTEND=noninteractive
LABEL org.opencontainers.image.authors="lu.chen.3@stonybrook.edu"
RUN apt -y update
RUN apt install -y build-essential libssl-dev cmake libboost-all-dev libgmp-dev libmpfr-dev libeigen3-dev libcgal-dev libcpprest-dev
WORKDIR /usr/src/server/build
COPY server ..
RUN cmake .. && make


FROM node:20-bookworm
RUN npm install pm2 -g
ENV NODE_ENV production
ENV PORT 8080

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y libssl-dev libboost-all-dev libgmp-dev libmpfr-dev libeigen3-dev libcgal-dev libcpprest-dev

USER node
WORKDIR /usr/src/app
COPY --chown=node:node --from=build /usr/src/server/build/generate_cell_ctpop .
COPY --chown=node:node download-data.sh .
RUN ./download-data.sh

COPY --chown=node:node package*.json ./
RUN npm ci
COPY --chown=node:node server.js ./

EXPOSE 8080
CMD [ "pm2-runtime", "server.js"]
