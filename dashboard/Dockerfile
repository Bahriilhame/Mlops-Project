FROM node:24-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL=http://localhost:8002
ARG VITE_MLFLOW_URL=http://localhost:5001
ARG VITE_DAGSTER_URL=http://localhost:4204
ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_MLFLOW_URL=${VITE_MLFLOW_URL}
ENV VITE_DAGSTER_URL=${VITE_DAGSTER_URL}
RUN npm run build

FROM nginx:stable-alpine AS production
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1/healthz || exit 1
CMD ["nginx", "-g", "daemon off;"]
