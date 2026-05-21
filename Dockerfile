# /opt/axentx/surrogate-1/Dockerfile

# Stage 1: Build
FROM golang:1.16 AS builder

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY *.go ./
RUN go build -o sidecar

# Stage 2: Production
FROM alpine:latest

RUN apk add --no-cache ca-certificates && \
    update-ca-certificates

WORKDIR /app

COPY --from=builder /app/sidecar .

ENTRYPOINT ["./sidecar"]