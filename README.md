# OpenDrive Framework

## Descripción
OpenDrive Framework es un proyecto open source diseñado para el desarrollo de sistemas de conducción autónoma. Proporciona la estructura y herramientas necesarias para crear un entorno completo de desarrollo.


## Estructura del Proyecto
El framework se divide en tres módulos principales:
- **Módulo de Sensores:** Captura información de la cámara y otros sensores.
- **Módulo de Percepción:** Realiza detecciones como carriles, señalamientos y objetos.
- **Módulo de Toma de Decisiones:** Define el comportamiento del vehículo basado en las detecciones obtenidas.

### Módulo de Sensores
El módulo de sensores incluye los paquetes `sensors` y `data_acquisition` los cuales son usados para la adquisision de datos, actualmente el unico sensor disponible es la camara.


### Módulo de Percepción
Este módulo hace uso de modelos de inteligencia artificial preentrenados donde se procesa la informacion obtenida por el módulo de sensores.

### Módulo de Toma de Decisiones
Este módulo obtendra las salidas proporcionadas por el modulo de percepción para procesarlas y dar información al usuario final.

## Instalación
Para instalar el framework, sigue estos pasos:
1. Clona el repositorio: `git clone https://github.com/tu_usuario/opendrive-framework.git`
2. Navega a la raiz del proyecto: `cd framework`
3. Instala las dependencias: `pip install -r requirements.txt`

## Uso
Puedes utilizar el framework siguiendo estas instrucciones:
```python
from opendrive import OpenDriveFramework

