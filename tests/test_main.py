from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ─── Usuarios ───────────────────────────────────────

def test_registro_usuario():
    response = client.post("/usuarios/", json={
        "nombre": "Test User",
        "email": "test_ci@email.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_registro_email_duplicado():
    client.post("/usuarios/", json={
        "nombre": "Test User",
        "email": "duplicado_ci@email.com",
        "password": "123456"
    })
    response = client.post("/usuarios/", json={
        "nombre": "Test User",
        "email": "duplicado_ci@email.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_login_exitoso():
    client.post("/usuarios/", json={
        "nombre": "Login Test",
        "email": "login_ci@email.com",
        "password": "123456"
    })
    response = client.post("/usuarios/login", json={
        "email": "login_ci@email.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_password_incorrecta():
    response = client.post("/usuarios/login", json={
        "email": "login_ci@email.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_login_usuario_no_existe():
    response = client.post("/usuarios/login", json={
        "email": "noexiste@email.com",
        "password": "123456"
    })
    assert response.status_code == 404

# ─── Categorías ─────────────────────────────────────

def test_listar_categorias_publico():
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_categoria_sin_token():
    response = client.post("/categorias/", json={
        "nombre": "Test Cat",
        "descripcion": "desc"
    })
    assert response.status_code == 401

# ─── Productos ──────────────────────────────────────

def test_listar_productos_publico():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_producto_sin_token():
    response = client.post("/productos/", json={
        "nombre": "Prod Test",
        "precio": 10.0,
        "stock": 5
    })
    assert response.status_code == 401

def test_producto_no_encontrado():
    response = client.get("/productos/99999")
    assert response.status_code == 404