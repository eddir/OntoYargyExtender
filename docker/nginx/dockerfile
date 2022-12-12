### STAGE 1: Build APP ###
FROM node:16.14 as builder-app
RUN npm config set unsafe-perm true && mkdir /app
COPY ./frontend /app/vue-client
WORKDIR /app/vue-client
RUN npm cache clean --force
RUN npm install
COPY . .
RUN npm run build

### STAGE 2: Nginx ###
FROM nginx:alpine as main
LABEL maintainer="ea@rostkov.me"

ENV TZ=UTC+3
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

## Copy our default nginx config
COPY ./docker/nginx/ /etc/nginx/conf.d/
COPY ./backend /app/backend
COPY --from=builder-app /app/vue-client/dist /app/vue-client

CMD ["nginx", "-g", "daemon off;"]
EXPOSE 443 80