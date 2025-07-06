### Run n8n locally in the main directory
```bash
docker-compose up -d 
```

Access n8n at http://localhost:5678


### Configuration of the mikrus.xyz server
New unix accounts:
```bash
sudo passwd root
sudo adduser mgzik
sudo usermod -aG sudo mgzik

w pliku /etc/ssh/sshd_config:
PermitRootLogin no

sudo systemctl restart sshd
```


Generate a self-signed SSL certificate for the domain xyz
```bash
## create self-signed SSL certificate
sudo openssl genrsa -out /etc/ssl/private/xyz.key 2048
sudo openssl req -new -x509 -key /etc/ssl/private/xyz.key -out /etc/ssl/certs/xyz.crt -days 760


## Create nginx configuration file for n8n
```bash
sudo vim /etc/nginx/sites-available/n8n
sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```
