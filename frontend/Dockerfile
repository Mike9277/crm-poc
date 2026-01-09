FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Installa con cache aggressivo
RUN npm install --no-audit --no-fund --prefer-offline --no-optional

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
