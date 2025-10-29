FROM node:20-slim AS builder
WORKDIR /app

# Copy package files
COPY from_loveable/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY from_loveable/ ./

# Build the app
RUN npm run build

# Production stage
FROM node:20-slim AS runner
WORKDIR /app

# Copy built assets
COPY --from=builder /app/dist ./dist

# Install serve to run the static site
RUN npm install -g serve

EXPOSE 8080
CMD ["serve", "-s", "dist", "-l", "8080"]