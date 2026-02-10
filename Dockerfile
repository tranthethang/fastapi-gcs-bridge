# Stage 1: Build dependencies
FROM python:3.10-alpine as builder

# Install build tools for C-based Python packages (if any)
RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app
COPY requirements.txt .

# Install dependencies to a temporary path
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Runtime
FROM python:3.10-alpine

ARG WWWUSER
ARG WWWGROUP

WORKDIR /app

# Create 'agent' user and group
RUN addgroup -g ${WWWGROUP} agent && \
    adduser -D -u ${WWWUSER} -G agent agent

# Copy installed libraries from builder stage
COPY --from=builder /install /usr/local

# Switch to non-root user
USER agent

# Default command for development (Port 80)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
