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
### Configuramos el I2C
I2C es un estandar usado usualmente para transferir informacion con distitos chips disponibles en el mercado, podemos comunicar nuestro Raspberry con distintos chips mediante i2c.
El bus i2c permite a multiples dispositivos conectarse con nuestro Raspberry Pi, cada uno con una diferente direccion, la cual frecuentemente puede ser cambiada desde el modulo.
Activaremos la comunicacion I2C de la siguiente forma
```
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```
Ingresamos al kernel para activar la comunicacion I2C

```
sudo raspi-config
```
Luego buscamos la opcion 'Interfacing Options', posteriormente entramos a 'I2C' (En versiones antiguas debemos de ingresar en 'Advanced Options').
Finalmente nos saldra una ventana que dira:
"Would you like the ARM I2C interface to be enable", le damos en <Yes>, finalmente.

```
sudo reboot
```
Cuando volvemos a ingresar testeamos I2C.
```
sudo i2cdetect -y 1
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

# Instalacion Libreria Scikit-Fuzzy

Necesitamos algunas librerias para poder correr Scikit-Fuzzy
```
pip install numpy
pip install scipy
pip install matplotlib
```
Una vez que hemos instalado las librerias instalamos git y scikit-fuzzy
```
sudo apt-get install git
(liiaarc)pi@raspberrypi~/liiaarc3 $ pip install scikit-fuzzy
```
Instalamos mediante PyP ya que es mas sencillo.

# Intalar Adafruit CircuitPython MCP4725
Instalaremos la libreria siguiendo esta [Guia](https://learn.adafruit.com/mcp4725-12-bit-dac-tutorial/python-circuitpython).
Nos aseguramos que nos encontramos en el environment.

```
cd liiaarc3
source bin/activate
pip3 install adafruit-adafruit-circuitpython-mcp4725
```

# Instalar Adafruit ADC Breakout ADS1115
Instalaremos la libreria siguiendo esta [guia](https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/assembly-and-wiring#multiple-boards-2-14).
Nos aseguramos que nos encontramos en el environment.

## Installing from PyPI
Podemos installar la libreria directamente desde pip3
```
cd liiaarc3
source bin/activate
pip3 install adafruit-circuitpython-ads1x15
```
