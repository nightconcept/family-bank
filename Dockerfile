# Dockerfile for Hugo Site

# --- Stage 1: Build Stage ---
# Use a specific version of the Hugo image.
FROM floryn90/hugo:0.145.0-alpine AS builder
# Using the image you specified in the logs.

WORKDIR /src

COPY . .

# Build the site into /tmp/public where the user should have write permissions.
# Added the '-d /tmp/public' flag to specify the destination.
RUN hugo --minify

# Stage 2: Serve the built site with Nginx
FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html
# Remove default Nginx welcome page
RUN rm -rf ./*
# Copy built site from the builder stage
COPY --from=builder /src/public .
# Expose port 80 for Nginx
EXPOSE 80
# Optional: Copy a custom nginx.conf if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]