# Usamos una imagen base de Python
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalamos las dependencias desde el archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de la aplicación al contenedor
COPY . .

# Comando por defecto para ejecutar la aplicación FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
