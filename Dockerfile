# --- Stage 1: Build Vite SPA ---
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package descriptors & configs
COPY package*.json tsconfig*.json vite.config.ts openapi.json ./
RUN npm ci --legacy-peer-deps

# Copy application source code
COPY . .

# Build Vite SPA production bundle
RUN npm run build

# --- Stage 2: Serve SPA with Nginx ---
FROM nginx:alpine AS runner
WORKDIR /usr/share/nginx/html

# Clean default Nginx files and copy Vite dist output
RUN rm -rf ./*
COPY --from=builder /app/dist ./

# SPA fallback configuration for client-side routing
RUN echo 'server { \
    listen 3000; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
