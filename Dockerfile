# Build
FROM node:12-alpine as build-step

RUN mkdir -p /app
# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @nrwl/cli

# add app
COPY . /app

RUN npm run build --prod --aot=true

ENV PROXY_USER "User"
ENV PROXY_USER "Pass"

# Run
FROM nginx:1.17.1-alpine

COPY --from=build-step /app/dist/apps/frontend /usr/share/nginx/html

EXPOSE 80
