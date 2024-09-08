# cap-3-tarea-3-api-mongo

## Configuración del Entorno y Ejecución del Proyecto FastAPI

Este documento describe los pasos necesarios para configurar un entorno de desarrollo virtual, instalar las dependencias del proyecto, y ejecutar la API en FastAPI.

### Prerrequisitos

Asegúrate de tener instalados los siguientes requisitos en tu máquina:

- Python 3.x
- `pip` (la herramienta de instalación de paquetes de Python)
- `virtualenv` (para crear entornos virtuales)

### 1. Crear un Entorno Virtual, activar el Entorno Virtual com git-bash, instalar las dependencias del requirements.txt y por último ejecutar la API FastAPI

```bash
virtualenv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### *Para desactivar el entorno virtual* `deactivate`

## (SENIOR DEVELOPER) POR FAVOR MEJORAR: 

1. Revisar el código y generar al menos una mejora al projecto. 

