FROM golang:latest AS builder
WORKDIR /build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o ./server ./main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /build/server .
EXPOSE 8080/tcp
CMD ["./server"]

# docker build -t ttn-receiver .
# docker run -d --name ttn-receiver --restart unless-stopped \
#     -v $(pwd)/ttn-receiver-data:/data \
#     --network proxynet \
#     ttn-receiver
