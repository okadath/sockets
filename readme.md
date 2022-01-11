## creacion del ambiente
ejecutar a mano los comandos de hand_install.sh y poner los valores del server en el archivo OnlineEXP-GLS

## agregar mensajes a la cola de redis

```py
python3 manage.py shell


import channels.layers
channel_layer = channels.layers.get_channel_layer()
from asgiref.sync import async_to_sync
async_to_sync(channel_layer.send)('default_preguntas', {'type': 'hello'})

async_to_sync(channel_layer.receive)('default_preguntas')

$ {'type': 'hello'}

async_to_sync(channel_layer.group_send)('chat_default_preguntas', {'type': 'chat_message', "message":"asdasdasd:vvv"})
```

## setear proyecto channels:

en el settings.py agregamos

```py
ASGI_APPLICATION = "Porsche.asgi.application" 

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

en el asgi.py agregamos el archivo donde van las routes de ws:

```py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# import chat.routing
import user_account.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Porsche.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            user_account.routing.websocket_urlpatterns
        )
    ),
})
```

creamos el routing.py(=urls.py):
```py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # /test_ws_preguntas/
    re_path(r'test_ws_preguntas/$', consumers.ChatConsumer.as_asgi()),

]
```
y creamos el consumer(=views.py):
```py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name='default_preguntas'
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("==========<zx<zx")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
```



## insertar elementos dinamicamente AlpineJS
```html
<!-- fragmento de como agregar elementos dinamicamente -->
<div x-data="addRemove()">
  <template x-for="(field, index) in fields" :key="field.id">
    <div>
      <input type="text" name="txt1[]" class="form-input">
      <button type="button" class="btn btn-danger btn-small" @click="removeField(field)">&times;</button>
    </div>
  </template>
  <button type="button" @click="addNewField()">+ Add Row</button>
</div>

<script type="text/javascript">
function addRemove() {
    return {
        fields: [],
        addNewField() {
            console.log(new Date().getTime() + this.fields.length);

            this.fields.push({id: new Date().getTime() + this.fields.length});
        },
        removeField(field) {
            this.fields.splice(this.fields.indexOf(field), 1);
        }
    }
}

</script>
```

## endpoint email
esta es su url, para no moverle a la instalacion no instale swagger
```
http://127.0.0.1:8000/POST/send_email
```




## Poblar la DB a partir de los archivos csv:

El script `feed.py` (solo necesita a Django como dependencia) convierte los datos de ese csv en datos listos para ser guardados en la DB usando el modulo Import-Export

Este script se usa con dos argumentos:
```
python  feed.py  eventbrite.csv  para_django.csv
```
**si no existe, creara `archivo_para_django.csv` automaticamente; si ya existe lo sobreescribe**
```
#ejemplo
python  feed.py  report-2020-10-14T1547-mexico-norte-pib.csv  Users.csv
```

### limpiar la DB
```sh
python manage.py shell
>>> from django.contrib.auth.models import User 
>>> User.objects.all().delete()
```

## Deploy
mientras el deploy no sea de cambios extremos bastarian 5 minutos para actualizar
deberias estar en `root@ubuntu:~/OnlineEXP` si no muevete a esa carpeta, una vez ahi cancela los commits

```sh
git reset --hard HEAD~1
git pull origin master
```
y reinicias gunicorn o no se veran los cambios

```
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```
si el status esta en verde funciono el update, si esta en rojo llora
y con eso ya se deployaron los cambios

si necesitamos guardar la db de produccion no tenemos de otra que pushearla desde el server de produccion o perderemos los datos que ingresen los usuarios

```
git push origin master
```
pusheamos a la fuerza y luego mergeamos


para la url de produccion:


sudo nano /etc/nginx/sites-available/myproject:
el inicio de ese archivo esta asi
```
server {
    listen 80;
    server_name X.X.X.X;
    ...

```

hay que cambiar la direccion numerica por nuestro dominio y regargar nginx y gunicorn:

```
sudo nginx -t
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl status gunicorn
sudo systemctl status nginx
```
si los dos estan en verde bastara con esperar uans horas para que la URL se propague en internet


## Creando el ambiente de desarrollo:

Para correr el proyecto en local, utilizamos pyenv
Para macos

Instalamos con brew:

```sh
brew install openssl readline sqlite3 xz zlib

pyenv install -v 3.7.2

```

En nuestra terminal vamos al directorio del proyecto y trabajamos con el ambiente virtual de python

```sh
pyenv init

eval "$(pyenv init -)"  

pyenv virtualenv env-OnlineEXP

pyenv activate env-OnlineEXP

pip install -r requirements.txt

python manage.py runserver

```

para poner la variable de la contraseña debes crear una variable en tu computadora, escribe esto en una shell (no importa la ubicacion) y dale enter:

```sh
export pass_mail="Password"
```

cada hosting tiene su manera de manejar las variables, lo unico que importa es NO PUSHEAR LA PASSWORD!

El email a usar debera terminar en `@gmail.com` y tener activadas las apps externas de google, para ello accede al siguiente link :
https://myaccount.google.com/lesssecureapps

y al final debe verse asi
https://github.com/vaaceves/OnlineEXP/blob/master/apps.png


tambien hay que activar este link
https://accounts.google.com/DisplayUnlockCaptcha

y ya permite el envio de emails

#### leyendo variables de entorno
para poner la contraseña del email o el keyid de la api como variable de entorno
en una shell escribimos la variable:
```sh
export my_var="asd"
```
para verla desde consola:
```sh
echo $my_var
```

para leer la variable desde python:
```py
import os
a = os.environ["my_var"]
print(a)
```




## vistas a formulario

es importante mantener el nombre en cada campo igual que el nombre del campo del modelo por que si no el POST de django no sabe a donde pasar ese dato en las vistas:
```html
<!-- aqui pasas el campo email de algun modelo -->
<input name="email" class="form-control" placeholder="Email" type="email">
```

las vistas del ciclo de usuarios las maneje en el views del user account, todo lo que sea de los eventos esta en los views de events

## editor de texto

django-ckeditor


la info del from viene en este fomrato, al aprecer  es esto en html `&lt;p&gt;aaaaaaaaaaaaaaa&lt;/p&gt;`
```
<tr><th><label for="id_content">Content:</label></th><td><div class="django-ckeditor-widget" data-field-id="id_content" style="display: inline-block;">
    <textarea cols="40" id="id_content" name="content" rows="10" required data-processed="0" data-config="{&quot;height&quot;: 291, &quot;skin&quot;: &quot;moono-lisa&quot;, &quot;width&quot;: 835, &quot;toolbar_Basic&quot;: [[&quot;Source&quot;, &quot;-&quot;, &quot;Bold&quot;, &quot;Italic&quot;]], &quot;language&quot;: &quot;en-us&quot;, &quot;filebrowserWindowWidth&quot;: 940, &quot;toolbar_Full&quot;: [[&quot;Styles&quot;, &quot;Format&quot;, &quot;Bold&quot;, &quot;Italic&quot;, &quot;Underline&quot;, &quot;Strike&quot;, &quot;SpellChecker&quot;, &quot;Undo&quot;, &quot;Redo&quot;], [&quot;Link&quot;, &quot;Unlink&quot;, &quot;Anchor&quot;], [&quot;Image&quot;, &quot;Flash&quot;, &quot;Table&quot;, &quot;HorizontalRule&quot;], [&quot;TextColor&quot;, &quot;BGColor&quot;], [&quot;Smiley&quot;, &quot;SpecialChar&quot;], [&quot;Source&quot;]], &quot;toolbar&quot;: &quot;Full&quot;, &quot;filebrowserWindowHeight&quot;: 725}" data-external-plugin-resources="[]" data-id="id_content" data-type="ckeditortype">&lt;p&gt;aaaaaaaaaaaaaaa&lt;/p&gt;
</textarea>
</div></td></tr>
```
si logro separarla y podemos convertir ese html en pdf tenemos la version de las notas


el servidor de archivos para imagenes tambiensirve para pdfs

```sh
asd=Post.objects.all()
>>> asd
<QuerySet [<Post: Post object (1)>, <Post: Post object (2)>]>
>>> asd[0]
<Post: Post object (1)>
>>> asd[0].text
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: 'Post' object has no attribute 'text'
>>> asd[0].content
'<p>asd</p>'
>>> asd[1].content
'<p>fddsf<img alt="cool" src="http://127.0.0.1:8000/static/ckeditor/ckeditor/plugins/smiley/images/shades_smile.png" style="height:23px; width:23px" title="cool" />sdf</p>'
```

equivalentes:
```html
<a href="{% url 'products:create_new_product' %}">...</a>
<form action="{% url 'products:create_new_product' %}">...</form>
```

DO
https://www.digitalocean.com/community/tutorials/como-configurar-django-con-postgres-nginx-y-gunicorn-en-ubuntu-18-04-es

## Dependencias pendejas para PDF y notes:
```sh
sudo apt install libcairo2-dev libsdl-pango-dev
```

## pasos activar el entorno en digital ocean

lo hice con venv alv por que la pendejada no distingue entre variables locales y globales en la instalacion o en el entorno, mamadas

hay que copiar la carpeta de static files al var/www para que el webserver las vea y las sirva me imagino que lo ideal es que estuvieran ahi siempre



tuve que tomar captura de pantalla por que el sistema de consola todo mierdoso no permite facilmente el copipasteo

force la pass en el local del arcivo settings a mano, al pushear se pierde, para no hacer merges hay que resetear el commit 
```
git reset --hard HEAD~1
```
aun no se como bajar la db, supongo que la subiremos comiteada a la fuerza o algo asi
https://www.digitalocean.com/community/questions/why-my-domain-is-not-working-in-nginx-django



sudo nano /etc/systemd/system/gunicorn.service :

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
Ss
[Service]
User=root
Group=www-data
WorkingDirectory=/home/OnlineEXP
ExecStart=/home/OnlineEXP/venv/bin/gunicorn  --access-logfile -  --workers 3  --bind unix:/run/gunicorn.sock  OnlineEXP.wsgi:application

[Install]
WantedBy=multi-user.target

```
sudo nano /etc/nginx/sites-available/OnlineEXP :

```
server {
    listen 80;
    server_name events.onel.media;
    #esto es para permitir archivos de mas de 100 MB
    client_max_body_size 100M;

    #location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/OnlineEXP/static/;#el nombre al final debe ir con /
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

```
sudo ln -s /etc/nginx/sites-available/OnlineEXP /etc/nginx/sites-enabled

este error en templates significa que no conoce el nombre de esa variable
```
NoReverseMatch at /event/

Reverse for 'join_event' with arguments '('',)' not found. 3 pattern(s) tried: ['event\\/join\\/(?P<name_event>[^/]+)$', 'join_event\\/$', 'join_event\\/$']
```
```
Cairocffi problems on local?
pip3 install -U pip
pip3 i`nstall -U setuptools
pip3 install --no-cache-dir cairocffi
```

## slugyfication

hay que descargar los modelos con import export, eliminarlos de la db, agregarlo y tambien onerle un default al slug en el models, y migrar, ya migrado importar y con el metodo `_get_unique_slug` se genera el slug de las instancias importadas  

##Celery

para el manejo de muchos envios de correo se debe de usar celery o se ralentiza

instalar
```sh
sudo apt install rabbitmq-server
pipenv install django-celery-email
```

en el init del proyecto base`OnlineEXP/__init__.py` agregamos lo siguiente para que cargue al iniciar el proyecto:
```py
from .celery import app as celery_app
__all__ = ['celery_app']
```
creamos en esa misma carpeta un achivo celery.py(al parecer es dificil configurarlo):
```py
# import os
# from celery import Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineEXP.settings')
# app = Celery('mysite')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineEXP.settings')
app = Celery('proj') #Nota 1
app.config_from_object('django.conf:settings', namespace='CELERY') #Nota 2
app.autodiscover_tasks() #Nota 3
# app.conf.update(
#     BROKER_URL = 'amqp://localhost:5672/', #Nota 4
# )
```

y en la app creamos la tarea a ejecutar `events/tasks.py`

```py
from OnlineEXP.celery import app
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@app.task
def enviar_mail(asunto, contenido, destinatario,img=""):
    # send_mail(asunto, contenido, 'noreply@mail.com', [destinatario], fail_silently=False)

    msg = EmailMessage(asunto, contenido, settings.EMAIL_HOST_USER,destinatario )
    msg.content_subtype = "html"
    if img!="":
        msg.attach_file(settings.BASE_DIR+"/"+img)
    msg.send()
```

y lo llamamos en las vistas usando `.delay()`:

```py
from events.tasks import enviar_mail
...
    texto_mail=request.POST["name"]+'\n'+request.POST["description"]
    asunto='Subject of the Email(TEST)'
    enviar_mail.delay(asunto, texto_mail, settings.DESTINATARIOS_ORACION,support.image.url)
```


```sh
#creamos la instancia de celery desviando la salida y el log al archivo
celery worker -A app_mail.celery &> celery.logs &
#si lo necesitamos matar llamamos lo siguiente
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill
#para ver si mato todos los workers
ps aux | grep -i celery
```

## archivos acentuados
en el OnlineEXP creamos un archivo llamado store.py:
```py
import unicodedata

from django.core.files.storage import FileSystemStorage

class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)
```
y lo agregamos al settings:
```py
DEFAULT_FILE_STORAGE = 'OnlineEXP.storage.ASCIIFileSystemStorage'
```

https://dnschecker.org/

para checar si ya se propagaron los DNS en internet

## Docker

instalacion
https://docs.docker.com/engine/install/ubuntu/
instalar docker compose
https://docs.docker.com/compose/install/#install-compose

usar:
```
sudo apt-get install apt-transport-https  ca-certificates curl  gnupg-agent software-properties-common
sudo add-apt-repository  "deb [arch=amd64] https://download.docker.com/linux/ubuntu  $(lsb_release -cs) stable"
```

para pushear sin meter siempre la pass(y sin el ssh, hice 128 builds en 2 dias, hubiera sido una locura en local)
```sh
git push https://username:password@myrepository.biz/file.git --all
```
comandos docker
```sh
docker ps = lista los contenedores

docker ps -a = lista contenedores a detalles

docker ps -aq = lista solo los ID de los contenedores (la q significa quiet, tranquilo o silencioso)

docker inspect id_contenedor = detalles internos del contenedor

docker inspect nombre_contenedor = lo mismo que el anterior

docker inspect -f {{}} nombre_contenedor = filtra una variable especifico del contenedor

docker rm nombre_contenedor = elimina un contenedor

docker rm $(ps -aq) = borra TODOS los contenedores
```


descargar el repo y crear el contenedor
```sh
docker-compose up -d --build
```
si hay un repo previo hay que darlo de baja:

```sh
docker-compose down -v
```

para entrar al contenedor:
```
docker exec -it test_dock_web_1 "/bin/bash"
```

para reiniciar el webserver, como ya esta la bandera always en el `docker-compose.yml` hay que matar el webserver y se reinicia en automatico, asi se actualizara al hacer modificaciones(pullear el repo)
```
docker-compose kill -s HUP web
```

## actualizar el server

entrar al container:
```sh
docker exec -it onlineexp-gls_web_1 "/bin/bash"
```

pullear/pushear:
```sh
#pushear cambios de la db a github
git add -A
git commit -m "magical commit"
git push origin main

#pullear desde github
git pull origin main
#si quieres eliminar los cambios en el repo(NO CON LA DB, solo en desarrollo)
git reset --hard HEAD~1
```

salir del repo (vuelves a la carpeta del proyecto):
```sh
exit
```

recargar el proceso del server()
```sh
docker-compose kill -s HUP web
```



## errores docker!

si algo ya consume el puerto 80 este no podra ser usado por el contenedor de nginx, por lo cual ha que matarlo (incluso si es una instalacion de nginx local)

## creacion ambiente

```sh
cd ../home/
apt-get update
git clone https://github.com/vaaceves/OnlineEXP-GLS
cd OnlineEXP-GLS
sudo chmod +x install.sh
sudo ./install.sh
docker-compose up -d --build
```


### Docker-ToDo:
ante el posible uso multiple de este proyecto iniciare a dockerizar el server de produccion
aun quedan muchas cosas por definir


+ deberian poderse mostrar muchos eventos y solo acceder a uno por codigo o mantener el multieventos?
+ el almacenamiento de archivos sera local o ya nos pasaremos a AWS(mucho mas complicado x q son eventos temporales)?
+ si se usaran muchas instancias podremos usar una pagina para controlar N deploys automaticamente en DOcean?


## testing artillery

```sh
yarn global add artillery
```

creamos un loadtest.yml con la configuracion de prueba
```yaml
config:
    target: "ws://127.0.0.1:8000/test_ws_preguntas/"
    ensure:
      maxErrorRate: 5
    phases:
      - duration: 30
        arrivalRate: 1
        rampTo: 10
        name: "Warming up"
      - duration: 50
        arrivalRate: 3
        rampTo: 200
        name: "Max load"
scenarios:
  - engine: "ws"
    flow:
      - send: "hello"
      - think: 2
      - send: "how are you?"
```
lo ejecutamos y nos crea un json, ese lo convierte a un reporte html

```sh
artillery run loadtest.yml --output result.json
artillery report result.json
```
