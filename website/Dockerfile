# Stage 1: Compile and Build angular codebase

# Use official node image as the base image
FROM node:18-alpine3.17 as build

# Set the working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY ./ /usr/local/app/

# Install all the dependencies
RUN npm install
#RUN npm install angular-mentions

# Generate the build of the application
# it's possible this might need to be updated to use environment.prod.ts
RUN npm run build

# Stage 2: Serve app with nginx server

# Use official nginx image as the base image
FROM nginx:latest

# Copy the build output to replace the default nginx contents.
COPY --from=build /usr/local/app/dist/website /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf  

# Expose port 80
EXPOSE 80