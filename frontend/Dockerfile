FROM node:20-alpine as builder

WORKDIR /build

COPY frontend/package.json .
RUN npm ci --only=production

FROM node:20-alpine

RUN addgroup -g 1000 -S appgroup && adduser -u 1000 -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/node_modules /app/node_modules

COPY --chown=appuser:appgroup frontend/ .

ENV NODE_ENV=production \
    PORT=3000

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000/ || exit(1)

CMD ["node", "app.js"]