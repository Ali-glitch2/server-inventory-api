from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Server Inventory API")


# The data a user must send when adding a server.
class Server(BaseModel):
    name: str
    ip_address: str
    environment: str  # for example: "dev", "staging" or "prod"


# Our "database": a simple list kept in memory.
# It is emptied every time the server restarts.
servers = []
next_id = 1


def find_server(server_id):
    """Find a server by its id, or send back a 404 error."""
    for server in servers:
        if server["id"] == server_id:
            return server
    raise HTTPException(status_code=404, detail="Server not found")


@app.get("/")
def home():
    return {"message": "Server Inventory API is running. Open /docs to try it."}


@app.get("/health")
def health():
    return {"status": "ok", "servers_saved": len(servers)}


@app.get("/servers")
def list_servers():
    """Show every saved server."""
    return servers


@app.get("/servers/{server_id}")
def get_server(server_id: int):
    """Show one server by its id."""
    return find_server(server_id)


@app.post("/servers", status_code=201)
def add_server(server: Server):
    """Save a new server."""
    global next_id

    # Do not allow two servers with the same name.
    for existing in servers:
        if existing["name"] == server.name:
            raise HTTPException(status_code=409, detail="A server with this name already exists")

    new_server = {
        "id": next_id,
        "name": server.name,
        "ip_address": server.ip_address,
        "environment": server.environment,
    }

    servers.append(new_server)
    next_id += 1
    return new_server


@app.delete("/servers/{server_id}")
def delete_server(server_id: int):
    server = find_server(server_id)
    servers.remove(server)
    return {"message": f"Deleted {server['name']}"}


@app.get("/servers/environment/{environment}")
def get_servers_by_environment(environment: str):
    matching = []
    for server in servers:
        if server["environment"] == environment:
            matching.append(server)
    return matching
