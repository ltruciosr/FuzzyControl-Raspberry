# MCP4725 - ADS1X15 / Raspberry PI
El conversor DAC MCP4725 de Adafruit es un dispositivo simple, pequeño, y facil de configurar.
Podemos aprovechar que posee un amplificador para realizar diversas tareas, y en este tutorial aprenderemos a usarlo.

# Getting Started
Para esta experiencia usaremos la libreria de Adafruit -CircuiPython-, primero debemos de instalar la libreria principal [Adafruit's CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).
Se recomienda crear un environment virtual para evitar problemas de compatibilidad entre versiones.
## Python Virtual Environment (virtualenv)
### Actualizamos el sistema
```
sudo apt-get update
sudo apt-get upgrade
```
### Instalamos virtualenv
```
sudo pip install virtualenv
```
### Creamos nuestro primer virtualenv
Primero debemos buscar donde se encuentra la version de python que queremos instalar (py2.7 en este caso)
```
which python 3.7
```
El terminal responde con: /usr/bin/python3.7
Usaremos la direccion para especificar la base del nuevo environment.
```
cd ~
virtualenv liiarc3 --python=/usr/bin/python3.7 --system-site-packages
```

Utilizamos --system-syte-packages, para instalar las librerias que se encuentran en el root de la version, ahora podemos activar el environment e instalar las librerias necesarias.
```
cd liiaarc3
source bin/activate
(liiaarc)pi@raspberrypi~/liiaarc3 $
```
# Circuit Python Library Installer
Para poder instalar las librerias de Adafruit, es necesario tener el root de las librerias, por lo cual necesitamos instalar Circuit Python.
### Instalar Adafruit CircuitPython Library Bundle
Una vez que nos encontramos en el environment [Guia](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).
```
cd ~/liiarc3
source bin/activate
pip install circuitpython-build-tools
```
Luego corremos el build.
```
cd ~
circuitpython-build-bundles --filename_prefix adafruit-circuitpython-bundle --library_location libraries --library_depth 2
``` 

# Intalar Adafruit CircuitPython MCP4725
Instalaremos la libreria siguiendo esta [Guia](https://learn.adafruit.com/mcp4725-12-bit-dac-tutorial/python-circuitpython).
Nos aseguramos que nos encontramos en el environment.
```
circuitpython-build-bundles --filename_prefix adafruit-circuitpython-mcp4725 --library_location .
```

# Instalar Adafruit ADC Breakout ADS1115
Instalaremos la libreria siguiendo esta [guia](https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring#multiple-boards-2-14).
Nos aseguramos que nos encontramos en el environment.

## Installing from PyPI
Podemos installar la libreria directamente desde pip3
```
pip3 install adafruit-circuitpython-ads1x15
```
Si queremos instalar en nuestro propio proyecto usamos.
```
cd ~/liiaarc3
source bin/activate
cd ~
circuitpython-build-bundles --filename_prefix adafruit-circuitpython-ads1x15 --library_location .
```

