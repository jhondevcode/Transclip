# Transclip

Este es un pequeño programa para usar la api de traduccion de google y traducir el texto que se encuentra en el portapapeles.

## Construyendo
Para poder construir el proyecto, requieres los siguiente:
- Python 3 o superior

El proyecto trabaja sobre un entorno virtual, esto se debe de crear a travez de virtualenv, para ello debes de instalarlo.

Ejecuta los siguientes comando de acurdo a tu sistema operativo:
- Para windows y mac -> ```pip install virtualenv```
- Para linux -> ```pip3 install virtualenv```

Una vez que tengas virtualenv instalado, clona el repositorio y ejectuta en la terminal la siguente linea para iniciar el entorno virtual:

```virtualenv Transclip``` __*esto iniciara el entorno virtual*__

Ahora lo que queda es __*activar*__ el entorno virtual:
- ``` cd Transclip ```
- Para windows y mac: ```/Scripts/activate ```
- Para linux: ``` source bin/activate ```

Por ultimo debemos de instalar los modulos necesarios para arrancar el proyecto:

- ``` pip install -r requeriments.txt ```