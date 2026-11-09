import json
import uuid
import hashlib
import platform
import socket
from datetime import datetime, timezone
from urllib.parse import parse_qs

def handle(event, context):
    if event.method == "GET":
        formulario = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Registro Serverless</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; padding: 50px 20px; }
        .contenedor { max-width: 450px; margin: auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #111; margin-bottom: 5px; }
        p { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        label { font-weight: bold; font-size: 14px; display: block; margin-top: 15px; color: #333; }
        input[type="text"], input[type="email"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        input[type="submit"] { width: 100%; padding: 12px; margin-top: 25px; background: #0066cc; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; }
        input[type="submit"]:hover { background: #004999; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Registro de Ejecución Serverless</h2>
        <p>Introducción al Cómputo de la Nube</p>
        <form method="POST">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" name="nombre" required>
            
            <label for="apellido">Apellido</label>
            <input type="text" id="apellido" name="apellido" required>
            
            <label for="email">Correo del aula virtual</label>
            <input type="email" id="email" name="email" required>
            
            <input type="submit" value="Generar archivo JSON">
        </form>
    </div>
</body>
</html>"""
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": formulario
        }

    elif event.method == "POST":
        cuerpo = event.body.decode("utf-8") if isinstance(event.body, bytes) else event.body
        datos = parse_qs(cuerpo)
        
        nombre = datos.get("nombre", [""])[0]
        apellido = datos.get("apellido", [""])[0]
        email = datos.get("email", [""])[0]
        
        token = str(uuid.uuid4())
        fecha_utc = datetime.now(timezone.utc).isoformat()
        
        cadena_firma = f"{nombre}{apellido}{email}{token}{fecha_utc}"
        firma = hashlib.sha256(cadena_firma.encode("utf-8")).hexdigest()
        
        resultado = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "token": token,
            "fecha_utc": fecha_utc,
            "sistema_operativo": platform.system(),
            "version_so": platform.version(),
            "arquitectura": platform.machine(),
            "procesador": platform.processor(),
            "version_python": platform.python_version(),
            "hostname_contenedor": socket.gethostname(),
            "plataforma": "OpenFaaS",
            "funcion": "registro-serverless",
            "estado": "Ejecucion exitosa",
            "firma_sha256": firma
        }
        
        contenido_json = json.dumps(resultado, indent=4, ensure_ascii=False)
        nombre_archivo = f"registro_{token}.json"
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Content-Disposition": f'attachment; filename="{nombre_archivo}"'
            },
            "body": contenido_json
        }