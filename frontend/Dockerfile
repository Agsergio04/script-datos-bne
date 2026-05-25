# ── Etapa 1: build ────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Recibe la URL del API como argumento de build (se "hornea" en el bundle de React)
ARG REACT_APP_API_URL=http://localhost:5000
ENV REACT_APP_API_URL=$REACT_APP_API_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ── Etapa 2: producción con nginx ──────────────────────────────
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
