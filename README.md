# Server Inventory API

A simple REST API built with **FastAPI** to keep track of servers: their name, IP address and environment (`dev`, `staging`, `prod`). Add servers, list them, look one up, filter by environment and delete them.

It is a lightweight version of the server inventory (CMDB) that DevOps teams use to know which machines they run and where.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.165-009688?logo=fastapi&logoColor=white)

---

## Features

- Add, list, view and delete servers
- Filter servers by environment
- Input validation with Pydantic (missing fields return `422`)
- Duplicate server names are rejected with `409 Conflict`
- Unknown server ids return `404 Not Found`
- Interactive API docs at `/docs`

## API endpoints

| Method | Endpoint | Description | Success code |
|--------|----------|-------------|--------------|
| GET | `/` | Welcome message | 200 |
| GET | `/health` | Health of the API and number of saved servers | 200 |
| GET | `/servers` | List all servers | 200 |
| GET | `/servers/{id}` | Get one server | 200 |
| GET | `/servers/environment/{environment}` | List servers in one environment | 200 |
| POST | `/servers` | Add a server | 201 |
| DELETE | `/servers/{id}` | Delete a server | 200 |

### Example: `POST /servers`

Request body:
```json
{ "name": "web-01", "ip_address": "10.0.0.1", "environment": "prod" }
```

Response (`201 Created`):
```json
{ "id": 1, "name": "web-01", "ip_address": "10.0.0.1", "environment": "prod" }
```

### Example: `GET /servers/environment/prod`

```json
[
  { "id": 1, "name": "web-01", "ip_address": "10.0.0.1", "environment": "prod" },
  { "id": 3, "name": "db-01", "ip_address": "10.0.0.3", "environment": "prod" }
]
```

### Error responses

| Code | When |
|------|------|
| `404` | Server id does not exist |
| `409` | A server with the same name already exists |
| `422` | A required field is missing or has the wrong type |

## Project structure

```
server-inventory-api/
├── app/
│   ├── __init__.py     # Marks "app" as a Python package
│   └── main.py         # The whole API
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting started

### Prerequisites
- Python 3.10 or newer

### Installation

```bash
git clone https://github.com/Ali-glitch2/server-inventory-api.git
cd server-inventory-api

python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Run

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** to try every endpoint in the browser.

## Usage with curl

```bash
# Add servers
curl -X POST http://127.0.0.1:8000/servers \
  -H "Content-Type: application/json" \
  -d '{"name": "web-01", "ip_address": "10.0.0.1", "environment": "prod"}'

# List all servers
curl http://127.0.0.1:8000/servers

# Only production servers
curl http://127.0.0.1:8000/servers/environment/prod

# Delete a server
curl -X DELETE http://127.0.0.1:8000/servers/1
```

**Windows PowerShell:**

```powershell
$body = @{ name = "web-01"; ip_address = "10.0.0.1"; environment = "prod" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/servers -ContentType "application/json" -Body $body
Invoke-RestMethod http://127.0.0.1:8000/servers/environment/prod
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Saved servers disappeared | Data is stored in memory and is cleared when the server restarts |
| `405 Method Not Allowed` | Wrong HTTP method, e.g. opening a POST endpoint in the browser. Use `/docs` |
| Endpoints return unexpected `404`s | Another process may be using port 8000. Check with `Get-NetTCPConnection -LocalPort 8000` (Windows) or `ss -tlnp` (Linux) |

## Limitations

- Servers are stored **in memory**, so they are lost when the API restarts.
- No update endpoint yet.

## Roadmap

- [ ] Store servers in a database
- [ ] Update a server (`PUT` / `PATCH`)
- [ ] Validate IP addresses and allowed environments
- [ ] Docker image

## What I learned

- Receiving JSON with **POST** and validating it with a **Pydantic** model
- Building create, read and delete endpoints for a resource
- Path parameters (`/servers/{id}`, `/servers/environment/{environment}`)
- Filtering a list with a loop
- Returning correct status codes (`201`, `404`, `409`, `422`) with `HTTPException`
- Debugging a port conflict caused by a leftover process

---

Built as **Day 2** of a 7-day FastAPI & backend challenge.
