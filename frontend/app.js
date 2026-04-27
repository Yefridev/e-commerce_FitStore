// URL base del backend — ajusta el puerto si es diferente
const API = "http://localhost:8000";

// ─────────────────────────────────────────
// PRODUCTOS — llama al backend real
// ─────────────────────────────────────────
async function cargarProductos() {
    const grid = document.getElementById("productosGrid");
    const loading = document.getElementById("loading");
    if (!grid) return;

    loading.style.display = "block";
    grid.innerHTML = "";

    try {
        const res = await fetch(`${API}/productos/`);
        if (!res.ok) throw new Error("Error al cargar productos");

        const productos = await res.json();
        loading.style.display = "none";

        if (productos.length === 0) {
            grid.innerHTML = "<p>No hay productos disponibles.</p>";
            return;
        }

        grid.innerHTML = productos.map(p => `
            <div class="card">
                <h3>${p.nombre}</h3>
                <p style="color:#666; font-size:0.9rem">${p.descripcion || "Sin descripción"}</p>
                <div class="precio">$${p.precio.toLocaleString()}</div>
                <div class="stock">Stock: ${p.stock} unidades</div>
                <button class="btn" onclick="agregarAlCarrito(${p.id})">
                    Agregar al carrito
                </button>
            </div>
        `).join("");

    } catch (err) {
        loading.innerHTML = `Error: ${err.message}`;
    }
}

async function cargarCategoriasFiltro() {
    const container = document.getElementById("categoriasFiltro");
    if (!container) return;

    try {
        const res = await fetch(`${API}/categorias/`);
        const categorias = await res.json();

        container.innerHTML = `<button class="btn" onclick="filtrarPorCategoria(0)" id="catBtn0" style="background:#e94560; margin-right:0.5rem; margin-bottom:0.5rem">Todos</button>`;

        categorias.forEach(c => {
            container.innerHTML += `<button class="btn" onclick="filtrarPorCategoria(${c.id})" id="catBtn${c.id}" style="margin-right:0.5rem; margin-bottom:0.5rem">${c.nombre}</button>`;
        });

        filtrarPorCategoria(0);

    } catch (err) {
        console.error("Error cargando categorías");
        cargarTodosProductos();
    }
}

async function filtrarPorCategoria(categoriaId) {
    const grid = document.getElementById("productosGrid");
    const loading = document.getElementById("loading");
    if (!grid) return;

    document.querySelectorAll("[id^='catBtn']").forEach(btn => {
        btn.style.background = "";
    });
    document.getElementById(`catBtn${categoriaId}`).style.background = "#e94560";

    loading.style.display = "block";
    loading.textContent = "Cargando...";
    grid.innerHTML = "";

    try {
        let productos;
        if (categoriaId === 0) {
            const res = await fetch(`${API}/productos/`);
            productos = await res.json();
        } else {
            const res = await fetch(`${API}/productos/categoria/${categoriaId}`);
            productos = await res.json();
        }

        loading.style.display = "none";

        if (productos.length === 0) {
            grid.innerHTML = "<p>No hay productos en esta categoría.</p>";
            return;
        }

        grid.innerHTML = productos.map(p => `
            <div class="card">
                <h3>${p.nombre}</h3>
                <p style="color:#666; font-size:0.9rem">${p.descripcion || "Sin descripción"}</p>
                <div class="precio">$${p.precio.toLocaleString()}</div>
                <div class="stock">Stock: ${p.stock} unidades</div>
                <button class="btn" onclick="agregarAlCarrito(${p.id})">
                    Agregar al carrito
                </button>
            </div>
        `).join("");

    } catch (err) {
        loading.innerHTML = `Error: ${err.message}`;
    }
}

// ─────────────────────────────────────────
// REGISTRO — con validación del lado cliente
// ─────────────────────────────────────────
async function registrar() {
    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    // Limpiar errores anteriores
    limpiarErrores();
    let valido = true;

    // Validaciones en el cliente (antes de llamar al backend)
    if (!nombre) {
        mostrarError("nombre", "errNombre");
        valido = false;
    }
    if (!email || !email.includes("@")) {
        mostrarError("email", "errEmail");
        valido = false;
    }
    if (password.length < 6) {
        mostrarError("password", "errPassword");
        valido = false;
    }

    if (!valido) return; // no llama al backend si hay errores

    try {
        // Llamada real al backend — POST /users/
        const res = await fetch(`${API}/usuarios/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre, email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            document.getElementById("alertError").textContent = data.detail || "Error al registrar";
            document.getElementById("alertError").style.display = "block";
            return;
        }

        // Éxito
        document.getElementById("alertSuccess").style.display = "block";
        setTimeout(() => mostrarLogin(), 2000);

    } catch (err) {
        document.getElementById("alertError").textContent = "No se pudo conectar al servidor";
        document.getElementById("alertError").style.display = "block";
    }
}

// ─────────────────────────────────────────
// LOGIN
// ─────────────────────────────────────────
async function login() {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
        const res = await fetch(`${API}/usuarios/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (!res.ok) {
            document.getElementById("alertLoginError").textContent = data.detail || "Credenciales incorrectas";
            document.getElementById("alertLoginError").style.display = "block";
            return;
        }

        // Guarda el token JWT para usarlo en peticiones autenticadas
        sessionStorage.setItem("token", data.access_token);
        sessionStorage.setItem("usuario", email);
        sessionStorage.setItem("usuario_id", data.id);
        sessionStorage.setItem("rol", data.rol);

        // Redirige a productos
        window.location.href = "/static/productos.html";

    } catch (err) {
        document.getElementById("alertLoginError").textContent = "No se pudo conectar al servidor";
        document.getElementById("alertLoginError").style.display = "block";
    }
}

// ─────────────────────────────────────────
// CARRITO
// ─────────────────────────────────────────
async function agregarAlCarrito(productoId) {
    const token = sessionStorage.getItem("token");

    if (!token) {
        alert("Debes iniciar sesión para agregar al carrito");
        window.location.href = "/";
        return;
    }

    const usuarioId = sessionStorage.getItem("usuario_id");
    if (!usuarioId) {
        alert("Error: usuario no identificado");
        return;
    }

    try {
        const res = await fetch(`${API}/carrito/${usuarioId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ producto_id: productoId, cantidad: 1 })
        });

        if (res.ok) {
            alert("Producto agregado al carrito");
        } else {
            const data = await res.json();
            alert(`Error: ${data.detail}`);
        }
    } catch (err) {
        alert("Error de conexión");
    }
}

// ─────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────
function mostrarError(inputId, errorId) {
    document.getElementById(inputId).classList.add("error");
    document.getElementById(errorId).style.display = "block";
}

function limpiarErrores() {
    ["nombre", "email", "password"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove("error");
    });
    ["errNombre", "errEmail", "errPassword"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });
    ["alertSuccess", "alertError"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    });
}

function mostrarLogin() {
    document.querySelector(".form-card").style.display = "none";
    document.getElementById("loginForm").style.display = "block";
}

function mostrarRegistro() {
    document.querySelector(".form-card").style.display = "block";
    document.getElementById("loginForm").style.display = "none";
}

// ─────────────────────────────────────────
// SESIÓN PERSISTENTE
// ─────────────────────────────────────────
function verificarSesionActiva() {
    const token = sessionStorage.getItem("token");
    if (token) {
        // Si hay sesión activa en la página de login, ir a home
        window.location.href = "/static/home.html";
    }
}

function guardarSesionPagina() {
    const path = window.location.pathname;
    // NO guardar index.html como página de sesión
    if (!path.includes("index.html") && path !== "/") {
        sessionStorage.setItem("sesion_pagina", path);
    }
}

function cerrarSesion() {
    if (!confirm("¿Cerrar sesión?")) return;

    sessionStorage.removeItem("token");
    sessionStorage.removeItem("usuario");
    sessionStorage.removeItem("usuario_id");
    sessionStorage.removeItem("rol");
    sessionStorage.removeItem("sesion_pagina");

    window.location.href = "/";
}

function guardarSesionPagina() {
    sessionStorage.setItem("sesion_pagina", window.location.pathname);
}

// Mostrar usuario en navbar si está logueado
const usuario = sessionStorage.getItem("usuario");
if (usuario) {
    const nav = document.getElementById("userNav");
    if (nav) nav.textContent = `👤 ${usuario}`;

    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) logoutBtn.style.display = "inline";

    guardarSesionPagina();
}

// Mostrar enlace Admin si es admin
const rol = sessionStorage.getItem("rol");
if (rol === "admin") {
    const adminLink = document.getElementById("adminLink");
    if (adminLink) adminLink.style.display = "inline";
}

// Verificar si hay sesión activa en index.html (página de login)
if (window.location.pathname === "/" || window.location.pathname === "/static/index.html") {
verificarSesionActiva();
}

// Cargar productos automáticamente si estamos en productos.html
if (window.location.pathname.includes("productos.html")) {
    cargarCategoriasFiltro();
}

// Verificar si es admin para mostrar panel admin
if (window.location.pathname.includes("admin.html")) {
    verificarAdmin();
}

async function crearProducto() {
    const token = sessionStorage.getItem("token");
    if (!token) {
        window.location.href = "/";
        return;
    }

    const nombre = document.getElementById("nombre").value.trim();
    const precio = parseFloat(document.getElementById("precio").value);
    const descripcion = document.getElementById("descripcion").value.trim();
    const stock = parseInt(document.getElementById("stock").value) || 0;
    const imagen = document.getElementById("imagen").value.trim();
    const categoria_id = document.getElementById("categoria_id").value || null;

    if (!nombre || isNaN(precio)) {
        mostrarAlerta("alertError", "El nombre y precio son requeridos");
        return;
    }

    try {
        const res = await fetch(`${API}/productos/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                nombre, precio, descripcion, stock, imagen,
                categoria_id: categoria_id ? parseInt(categoria_id) : null
            })
        });

        if (!res.ok) {
            const data = await res.json();
            mostrarAlerta("alertError", data.detail || "Error al crear producto");
            return;
        }

        mostrarAlerta("alertSuccess", "Producto creado exitosamente");
        setTimeout(() => {
            cargarProductosList();
            limpiarFormProducto();
        }, 1000);
    } catch (err) {
        mostrarAlerta("alertError", "Error de conexión");
    }
}

async function crearCategoria() {
    const token = sessionStorage.getItem("token");
    if (!token) {
        window.location.href = "/";
        return;
    }

    const nombre = document.getElementById("catNombre").value.trim();
    const descripcion = document.getElementById("catDescripcion").value.trim();

    if (!nombre) {
        mostrarAlerta("alertError", "El nombre es requerido");
        return;
    }

    try {
        const res = await fetch(`${API}/categorias/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ nombre, descripcion })
        });

        if (!res.ok) {
            const data = await res.json();
            mostrarAlerta("alertError", data.detail || "Error al crear categoría");
            return;
        }

        mostrarAlerta("alertSuccess", "Categoría creada exitosamente");
        setTimeout(() => {
            cargarCategoriasAdmin();
            cargarCategoriasList();
            document.getElementById("catNombre").value = "";
            document.getElementById("catDescripcion").value = "";
        }, 1000);
    } catch (err) {
        mostrarAlerta("alertError", "Error de conexión");
    }
}

async function cargarCategoriasList() {
    try {
        const res = await fetch(`${API}/categorias/`);
        const categorias = await res.json();

        const container = document.getElementById("categoriasList");
        if (!container) return;

        if (categorias.length === 0) {
            container.innerHTML = "<p>No hay categorías.</p>";
            return;
        }

        container.innerHTML = categorias.map(c => `
            <div style="padding:0.5rem; border-bottom:1px solid #eee">
                <strong>${c.nombre}</strong>
                <span style="color:#888"> - ${c.descripcion || "Sin descripción"}</span>
            </div>
        `).join("");
    } catch (err) {
        console.error("Error cargando categorías");
    }
}

async function cargarProductosList() {
    const token = sessionStorage.getItem("token");
    try {
        const res = await fetch(`${API}/productos/`);
        const productos = await res.json();

        const container = document.getElementById("productosList");
        if (!container) return;

        if (productos.length === 0) {
            container.innerHTML = "<p>No hay productos.</p>";
            return;
        }

        container.innerHTML = productos.map(p => `
            <div style="padding:0.5rem; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center">
                <div>
                    <strong>${p.nombre}</strong>
                    <span style="color:#e94560"> - $${p.precio}</span>
                    <span style="color:#888"> | Stock: ${p.stock}</span>
                </div>
                <button class="btn" style="padding:0.3rem 0.8rem; font-size:0.8rem" onclick="eliminarProducto(${p.id})">Eliminar</button>
            </div>
        `).join("");
    } catch (err) {
        console.error("Error cargando productos");
    }
}

async function eliminarProducto(productoId) {
    const token = sessionStorage.getItem("token");
    if (!confirm("¿Eliminar este producto?")) return;

    try {
        const res = await fetch(`${API}/productos/${productoId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            alert("Error al eliminar producto");
            return;
        }

        cargarProductosList();
    } catch (err) {
        alert("Error de conexión");
    }
}

function mostrarAlerta(id, mensaje) {
    const el = document.getElementById(id);
    el.textContent = mensaje;
    el.style.display = "block";
    setTimeout(() => el.style.display = "none", 3000);
}

function limpiarFormProducto() {
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("descripcion").value = "";
    document.getElementById("stock").value = "0";
    document.getElementById("imagen").value = "";
    document.getElementById("categoria_id").value = "";
}

// ─────────────────────────────────────────
// ADMIN — verificar y cargar datos
// ─────────────────────────────────────────
async function verificarAdmin() {
    const token = sessionStorage.getItem("token");
    const rol = sessionStorage.getItem("rol");

    if (!token || rol !== "admin") {
        alert("Acceso restringido. Solo administradores.");
        window.location.href = "/";
        return;
    }

    // Cargar categorías en el select del formulario
    await cargarCategoriasAdmin();
    // Cargar listas
    await cargarCategoriasList();
    await cargarProductosList();
}

async function cargarCategoriasAdmin() {
    try {
        const res = await fetch(`${API}/categorias/`);
        const categorias = await res.json();

        const select = document.getElementById("categoria_id");
        if (!select) return;

        // Limpiar opciones anteriores y dejar solo "Sin categoría"
        select.innerHTML = `<option value="">Sin categoría</option>`;

        // Agregar cada categoría como opción
        categorias.forEach(c => {
            select.innerHTML += `<option value="${c.id}">${c.nombre}</option>`;
        });

    } catch (err) {
        console.error("Error cargando categorías para el select");
    }
}