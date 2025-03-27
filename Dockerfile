# Dockerfile for Hugo Site

# --- Stage 1: Build Stage ---
# Use a specific version of the Hugo image (extended version includes SASS/SCSS support).
# Using Alpine base for smaller size. Check for newer versions if needed: https://github.com/klakegg/docker-hugo/tags
FROM floryn90/hugo:0.145.0-alpine AS builder
# You can change the Hugo version tag above if your project requires a different one.

# Set the working directory inside the container
WORKDIR /src

# Copy your Hugo project files into the container
# This includes content/, static/, themes/, config files (hugo.toml), etc.
COPY . .

# Build the Hugo site.
# The --minify flag reduces the size of HTML, CSS, JS files.
# Hugo builds the site into the `/src/public` directory by default.
# Note: If your theme is a Git submodule, this simple COPY won't include it.
# You might need a more complex build stage involving git clone if using submodules.
RUN hugo --minify


# --- Stage 2: Runtime Stage ---
# Use a lightweight Nginx image to serve the static files
FROM nginx:stable-alpine AS runner

# Copy the built static site files from the 'builder' stage's '/src/public' directory
# into the default Nginx public HTML directory.
COPY --from=builder /src/public /usr/share/nginx/html

# (Optional) Copy a custom Nginx configuration file if you need specific rules
# (e.g., for redirects, headers, or SPA routing if Hugo is just part of a larger app).
# If you create an nginx.conf file in your project root, uncomment the next line:
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (the default port Nginx listens on)
EXPOSE 80

# The base Nginx image already has a CMD ["nginx", "-g", "daemon off;"]
# which starts Nginx in the foreground, so we don't need to specify it again
# unless overriding the default config requires a different command.