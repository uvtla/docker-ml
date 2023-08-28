FROM node:20.0.0 as build

WORKDIR /app

COPY public public
COPY src src
COPY index.html package.json vite.config.ts ./
RUN npm i && npm run build

FROM nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /app
COPY --from=build /app/dist .

