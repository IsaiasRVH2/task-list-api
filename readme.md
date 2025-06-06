# 📝 Task List API
Una API RESTful construida con FastAPI para gestionar tareas personales. La API permite a los usuarios registrarse, iniciar sesión y realizar operaciones CRUD sobre sus tareas.

## 🚀 Características
* Registro y autenticación de usuarios con JWT.
* Creación, lectura, actualización y eliminación de tareas.
* Protección de endpoints con dependencias de autenticación.
* Validación de datos con Pydantic.
* Base de datos relacional con SQLAlchemy y PostgreSQL.
* Test  automáticos con pytest y httpx.

## 📦 Tecnologías utilizadas
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Pydantic](https://docs.pydantic.dev/)
* [Alembic](https://alembic.sqlalchemy.org/) (migraciones)
* [httpx](https://www.python-httpx.org/) y [Pytest](https://docs.pytest.org/en/stable/) (tests) 
* [Uvicorn](https://www.uvicorn.org/) (servidor ASGI)

## ⚙️ Instalación
```bash
# Bash

# Clonar el repositorio
git clone https://github.com/IsaiasRVH2/task-list-api.git

# Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate # En windows: venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta las migraciones (si usas Alembic)
alembic upgrade head

# Ejecuta la aplicación
python -m uvicorn app.main:app --reload
```

## 🔐 Autenticación
Esta API usa JWT (JSON Web Tokens) para acceder a los endpoints protegidos:
1. Regístrate en ```/api/users/```
2. Inicia sesión en ```/api/login/``` y obten el token de acceso.
3. Usa el token de acceso en la cabecera ```Authorization```:
    ```makefile
    Authorization: Bearer <token>
    ```

## 📚 Endpoints principales
| Método | Ruta            | Descripción                  |
| ------ | --------------- | ---------------------------- |
| POST   | /api/users/     | Registrar nuevo usuario      |
| POST   | /api/login/     | Obtener token de acceso      |
| GET    | /api/users/me   | Obtener datos del usuario    |
| PUT    | /api/users/me   | Actualizar datos del usuario |
| POST   | /api/tasks/     | Crear nueva tarea            |
| GET    | /api/tasks/     | Listar tareas del usuario    |
| GET    | /api/tasks/{id} | Obtener detalle de una tarea |
| PUT    | /api/tasks/{id} | Actualizar una tarea         |
| DELETE | /api/tasks/{id} | Eliminar una tarea           |


## 📁 Estructura del proyecto
```css
task-list-api/
├── alembic/                         
├── app/
│   ├── main.py                     
│   ├── api/
│   │   └── routes/                 
│   │       ├── auth.py
│   │       ├── tasks.py
│   │       └── users.py
│   ├── core/                       
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── crud/                       
│   │   ├── task.py
│   │   └── user.py
│   ├── models/                     
│   │   ├── base.py
│   │   ├── task.py
│   │   └── user.py
│   ├── schemas/                    
│   │   ├── task.py
│   │   ├── token.py
│   │   ├── user.py
│   └── exceptions.py
├── tests/                          
│   ├── conftest.py                 
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── test_users.py
├── requirements.txt                
└── README.md                       
```

## 📌 Estado del proyecto
✅ Funcionalidades básicas completas

🔄 En desarrollo: permisos avanzados, test unitarios para tasks y autenticación, test de integración.

## 🧑 Autor
Desarrollado por Isaías Ricardo Valdivia

[GitHub](https://github.com/IsaiasRVH2/)
|
[Linkedin](https://www.linkedin.com/in/isaias-valdivia/)