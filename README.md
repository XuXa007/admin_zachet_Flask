   ```bash
   python3 -V
   mkdir -p /home/xuxa/ap
   cd app/
journalctl -u flaskapp.service
   
sudo lsof -i :80
sudo kill -9 <PID>

   apt install python3.10-venv
   python3 -m venv venv

sudo nano web_server_zachet.py 
sudo nano /etc/systemd/system/flaskapp.service 
udo nano /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-available/default
   ```

Зайти в окружение
  ```bash
  source venv/bin/activate
  ```
Выйти
  ```bash
  deactivate
  ```
Первый этап
```
git clone git@github.com:XuXa007/app.git
ls
cd app
```

Перейдите в директорию вашего приложения
```
cd /home/xuxa/app
```
Создаем виртуальную среду
```
# не делала сразу с source
python3 -m venv venv
```
Активируем виртуальную среду
```
source venv/bin/activate
```
Установим Flask
```
sudo apt install python3-pip
pip install Flask
```

Идем в конфиг
```
sudo nano /etc/systemd/system/flaskapp.service
```
```text
[Unit]
Description=Flask Application
After=network.target

[Service]
User=xuxa
Group=www-data
WorkingDirectory=/home/xuxa/app
Environment="PATH=/home/xuxa/app/venv/bin"
ExecStart=/usr/bin/python3 /home/xuxa/app/web_server_zachet.py

[Install]
WantedBy=multi-user.target

```
Но надо посмотреть ExecStart - ```bash which python3``` - /usr/bin/python3. 

/home/xuxa/app/web_server_zachet.py - путь до .py

Запускаем Flask
```
sudo systemctl daemon-reload
sudo systemctl start flaskapp.service
sudo systemctl enable flaskapp.service
```

Проверяем
```
sudo systemctl status flaskapp.service
```
Если все хорошо - active (running) - то идем дальше

Установка Nginx
```
sudo apt update
sudo apt install nginx
sudo nginx -t
```

НЕ пригодилось
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/



Идем в конфиг
```
sudo nano /etc/nginx/sites-available/default
```

Пишем 
```
server {
    listen 80;
    server_name server;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
ИЛИ 

sudo nano /etc/nginx/sites-available/flaskapp

Пишем

server {
    listen 80;
    server_name server;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

НО И В ``` sudo nano /etc/nginx/sites-enabled/default```

НЕ пригодилось
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/



Проверяем
```
sudo nginx -t
```
Рестартим
```
sudo systemctl restart nginx
sudo systemctl status nginx
```

(venv) xuxa@ubuntu:~/app$ sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-05-27 23:21:12 UTC; 7s ago
       Docs: man:nginx(8)
    Process: 1299 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 1300 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 1302 (nginx)
      Tasks: 3 (limit: 2191)
     Memory: 3.2M
        CPU: 19ms
     CGroup: /system.slice/nginx.service
             ├─1302 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             ├─1303 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" ""
             └─1304 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" ""

May 27 23:21:12 ubuntu systemd[1]: Starting A high performance web server and a reverse proxy server...
May 27 23:21:12 ubuntu systemd[1]: Started A high performance web server and a reverse proxy server.
(venv) xuxa@ubuntu:~/app$ 


Если ошибка Failed to start A high performance web server and a reverse proxy server. при sudo systemctl status nginx
значит занят порт 

Решение:
```
sudo lsof -i :80
sudo kill -9 <PID>
```

Или в моем случае 
```
sudo systemctl stop apache2
```

Обновляем 
```
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl status nginx
```

если все хорошо -  active (running) - идем дальше

Проверям в терминале
```
curl http://127.0.0.1:5000/
```
```
ip a
```
```
http://{192.168.1.9}
```



