docker run -d \
    --name dbase_cont \
    --network net_app_dbase \
    -e POSTGRES_USER=danya \
    -e POSTGRES_PASSWORD=123 \
    -e POSTGRES_DB=dbase \
    postgres:15-alpine

docker run -d \
    --name app_cont \
    --network net_app_dbase \
    app_img

docker run -d \
    --name nginx_server \
    --network net_app_dbase \
    -p 80:80 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
    -v $(pwd)/placeholder.html:/usr/share/nginx/html/placeholder.html:ro \
    -v $(pwd)/ip.txt:/etc/nginx/ip.txt:ro \
    nginx:alpine