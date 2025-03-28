# Dockerfile.nginx
# This Dockerfile is used ONLY by the deploy job on the self-hosted runner.
# It expects the 'public' directory (built in the 'build' job) to be available in the build context.

FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html

# Clean out default Nginx content
RUN rm -rf ./*

# Copy the pre-built 'public' directory from the build context
COPY public .

# Expose the port Nginx listens on (adjust if your Nginx config differs)
# Make sure this matches the port in your Traefik service label!
EXPOSE 80

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]