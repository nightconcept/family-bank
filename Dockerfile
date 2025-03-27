# Dockerfile for Hugo Site

# --- Stage 1: Build Stage ---
# Use a specific version of the Hugo image.
FROM floryn90/hugo:0.145.0-alpine AS builder
# Using the image you specified in the logs.

WORKDIR /src

COPY . .

# Build the site into /tmp/public where the user should have write permissions.
# Added the '-d /tmp/public' flag to specify the destination.
RUN hugo --minify -d /tmp/public

# --- Stage 2: Runtime Stage ---
FROM nginx:stable-alpine AS runner

# Copy the built static files from the 'builder' stage's '/tmp/public' directory
# Updated path from /src/public to /tmp/public
COPY --from=builder /tmp/public /usr/share/nginx/html

# (Optional) Copy a custom Nginx configuration file if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"] # Inherited from base image