# frontend_services/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package.json and package-lock.json from the telemed subfolder
COPY telemed/package*.json ./

# Install deps
RUN npm install

# Copy the rest of the React app
COPY telemed/ ./

# Expose React dev server port
EXPOSE 3000

# Start the React dev server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]