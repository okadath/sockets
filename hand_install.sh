sudo apt install python3-pip python3-dev libpq-dev  nginx curl libcairo2-dev libsdl-pango-dev python3-certbot-nginx

sudo -H pip3 install virtualenv
virtualenv venv
source venv/bin/activate



pip install -r requirements.txt
pip install  gunicorn
cp gunicorn.socket /etc/systemd/system/gunicorn.socket
cp gunicorn.service /etc/systemd/system/
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.socket
sudo systemctl daemon-reload
sudo cp OnlineEXP-GLS /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/OnlineEXP-GLS /etc/nginx/sites-enabled


sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
sudo certbot --nginx -d example.com 
sudo systemctl restart gunicorn