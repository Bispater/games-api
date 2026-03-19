# Games Kiosk API

API REST pura para el kiosko de juegos interactivos. Sin frontend — el admin visual vive dentro de `games-kiosk`.

- **Backend**: Django 5.1 + Django REST Framework
- **Base de datos**: SQLite (local) / PostgreSQL (producción)
- **Concepto**: Cada cliente tiene un código (ej: `ENT01`). El kiosk pide su config con ese código.

---

## Ejecución Local

```bash
cd games-kiosk-api

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python manage.py migrate

# Crear superusuario (para Django admin en /admin/)
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver 8000
```

La API estará en: **http://localhost:8000/api/**
Django admin en: **http://localhost:8000/admin/**

## Ejecución con Docker

```bash
cd games-kiosk-api
docker-compose up --build
```

---

## Endpoints API

### Clientes (Configuraciones)
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/clients/` | Listar todos los clientes |
| POST | `/api/clients/` | Crear nuevo cliente |
| GET | `/api/clients/ENT01/` | Config completa (formato compatible con games-kiosk) |
| PUT | `/api/clients/ENT01/` | Actualizar config completa |
| PATCH | `/api/clients/ENT01/` | Actualizar campos parciales |
| DELETE | `/api/clients/ENT01/` | Eliminar cliente |
| POST | `/api/clients/ENT01/upload-logo/` | Subir logo (multipart) |
| POST | `/api/clients/ENT01/upload-favicon/` | Subir favicon (multipart) |

### Leaderboard
| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/leaderboard/?client=ENT01&game_id=memory` | Listar entradas (filtros opcionales) |
| POST | `/api/leaderboard/` | Crear entrada `{client_code, game_id, player_name, score, ...}` |
| DELETE | `/api/leaderboard/{id}/` | Eliminar entrada |
| GET | `/api/leaderboard/top/ENT01/memory/?limit=10` | Top scores por cliente y juego |
| DELETE | `/api/leaderboard/clear/?client=ENT01&game_id=memory` | Limpiar (params opcionales) |

---

## Integración con games-kiosk

El kiosk debe obtener su config haciendo fetch a:

```
GET http://localhost:8000/api/clients/ENT01/
```

La respuesta tiene el **mismo formato** que `client-config.json`:

```json
{
  "code": "ENT01",
  "client": { "name": "Entel", "subtitle": "...", "logo": "...", "favicon": "..." },
  "branding": { "primaryColor": "#1400FF", ... },
  "kiosk": { "exitPassword": "1234", ... },
  "games": { "memory": { "enabled": true, "pairs": 8 }, ... },
  "records": { "enabled": true, ... }
}
```

El admin visual para gestionar esto está en **games-kiosk** bajo la ruta `/admin`.
