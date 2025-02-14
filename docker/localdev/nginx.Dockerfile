FROM nginx:latest

# Копіюємо конфігураційний файл Nginx
COPY docker/localdev/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
