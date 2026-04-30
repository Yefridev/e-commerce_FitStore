const API = "http://localhost:8000";

// ─────────────────────────────────────────
// INICIALIZACIÓN Y ROLES
// ─────────────────────────────────────────
function inicializarRoles() {
    const rol = sessionStorage.getItem("rol");
    const usuario = sessionStorage.getItem("usuario");
    const token = sessionStorage.getItem("token");

    // Mostrar usuario en navbar
    if (usuario && token) {
        const nav = document.getElementById("userNav");
        if (nav) nav.textContent = `👤 ${usuario}`;
        
        const logoutBtn = document.getElementById("logoutBtn");
        if (logoutBtn) logoutBtn.style.display = "inline";
    }

    // Mostrar enlaces según rol
    if (rol === "admin") {
        // Admin: mostrar panel admin
        document.querySelectorAll(".admin-only").forEach(el => {
            el.classList.add("show");
            el.style.display = "inline-block";
        });
        const adminLink = document.getElementById("adminLink");
        if (adminLink) adminLink.style.display = "inline";
        const adminBtn = document.getElementById("adminBtn");
        if (adminBtn) adminBtn.style.display = "inline-block";
    } else if (rol === "cliente") {
        // Cliente: mostrar carrito y funciones de compra
        document.querySelectorAll(".client-only").forEach(el => {
            el.classList.add("show");
            el.style.display = "inline-block";
        });
        document.querySelectorAll(".client-only.show-block").forEach(el => {
            el.style.display = "block";
        });
    }

    // Logos consistentes
    setLogoHrefs();
}

function setLogoHrefs() {
    const token = sessionStorage.getItem("token");
    const targetHref = token ? "/static/home.html" : "/static/index.html";
    document.querySelectorAll("a.logo").forEach(logo => {
        logo.href = targetHref;
    });
}

// ─────────────────────────────────────────
// PRODUCTOS
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
            grid.innerHTML = "<p style='color:#BFBFBF'>No hay productos disponibles.</p>";
            return;
        }

        const esCliente = sessionStorage.getItem("rol") === "cliente";

        grid.innerHTML = productos.map(p => `
            <div class="card">
                <h3>${p.nombre}</h3>
                <p style="color:#BFBFBF; font-size:0.9rem">${p.descripcion || "Sin descripción"}</p>
                <div class="precio">$${p.precio.toLocaleString()}</div>
                <div class="stock" style="color:#BFBFBF">Stock: ${p.stock} unidades</div>
                ${esCliente ? `<button class="btn" onclick="agregarAlCarrito(${p.id})">Agregar al carrito</button>` : ''}
            </div>
        `).join("");

    } catch (err) {
        loading.innerHTML = `<span style="color:#FF3B3B">Error: ${err.message}</span>`;
    }
}

async function cargarCategoriasFiltro() {
    const container = document.getElementById("categoriasFiltro");
    if (!container) return;

    try {
        const res = await fetch(`${API}/categorias/`);
        const categorias = await res.json();

        container.innerHTML = `<button class="btn" onclick="filtrarPorCategoria(0)" id="catBtn0" style="background:#FF3B3B; margin-right:0.5rem; margin-bottom:0.5rem">Todos</button>`;
        categorias.forEach(c => {
            container.innerHTML += `<button class="btn" onclick="filtrarPorCategoria(${c.id})" id="catBtn${c.id}" style="margin-right:0.5rem; margin-bottom:0.5rem">${c.nombre}</button>`;
        });
        filtrarPorCategoria(0);

    } catch (err) {
        console.error("Error cargando categorías");
        cargarProductos();
    }
}

async function filtrarPorCategoria(categoriaId) {
    const grid = document.getElementById("productosGrid");
    const loading = document.getElementById("loading");
    if (!grid) return;

    document.querySelectorAll("[id^='catBtn']").forEach(btn => btn.style.background = "");
    const activeBtn = document.getElementById(`catBtn${categoriaId}`);
    if (activeBtn) activeBtn.style.background = "#FF3B3B";

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
            grid.innerHTML = "<p style='color:#BFBFBF'>No hay productos en esta categoría.</p>";
            return;
        }

        const esCliente = sessionStorage.getItem("rol") === "cliente";

        grid.innerHTML = productos.map(p => `
            <div class="card">
                <h3>${p.nombre}</h3>
                <p style="color:#BFBFBF; font-size:0.9rem">${p.descripcion || "Sin descripción"}</p>
                <div class="precio">$${p.precio.toLocaleString()}</div>
                <div class="stock" style="color:#BFBFBF">Stock: ${p.stock} unidades</div>
                ${esCliente ? `<button class="btn" onclick="agregarAlCarrito(${p.id})">Agregar al carrito</button>` : ''}
            </div>
        `).join("");

    } catch (err) {
        loading.innerHTML = `<span style="color:#FF3B3B">Error: ${err.message}</span>`;
    }
}

// ─────────────────────────────────────────
// REGISTRO
// ─────────────────────────────────────────
async function registrar() {
    const nombre = document.getElementById("nombre").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    limpiarErrores();
    let valido = true;

    if (!nombre) { mostrarError("nombre", "errNombre"); valido = false; }
    if (!email || !email.includes("@")) { mostrarError("email", "errEmail"); valido = false; }
    if (password.length < 6) { mostrarError("password", "errPassword"); valido = false; }

    if (!valido) return;

    try {
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

        sessionStorage.setItem("token", data.access_token);

        // Obtener perfil para id y rol
        const profileRes = await fetch(`${API}/usuarios/mi-perfil`, {
            headers: { "Authorization": `Bearer ${data.access_token}` }
        });
        if (!profileRes.ok) {
            sessionStorage.clear();
            throw new Error("Error al obtener perfil");
        }
        const profile = await profileRes.json();
        sessionStorage.setItem("usuario_id", profile.id);
        sessionStorage.setItem("rol", profile.rol);
        sessionStorage.setItem("usuario", profile.nombre);

        window.location.href = "/static/home.html";

    } catch (err) {
        document.getElementById("alertLoginError").textContent = err.message || "No se pudo conectar al servidor";
        document.getElementById("alertLoginError").style.display = "block";
    }
}

// ─────────────────────────────────────────
// CARRITO - FUNCIONES PARA CLIENTES
// ─────────────────────────────────────────
async function agregarAlCarrito(productoId) {
    const token = sessionStorage.getItem("token");
    if (!token) {
        alert("Debes iniciar sesión para agregar al carrito");
        window.location.href = "/";
        return;
    }

    try {
        const res = await fetch(`${API}/carrito/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ producto_id: productoId, cantidad: 1 })
        });

        if (res.ok) {
            alert("Producto agregado al carrito");
            actualizarCartCount();
        } else {
            const data = await res.json();
            alert(`Error: ${data.detail}`);
        }
    } catch (err) {
        alert("Error de conexión");
    }
}

async function verCarrito() {
    const token = sessionStorage.getItem("token");
    if (!token) {
        alert("Debes iniciar sesión");
        window.location.href = "/";
        return;
    }

    const container = document.getElementById("carritoContainer");
    if (!container) return;

    try {
        const res = await fetch(`${API}/carrito/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!res.ok) throw new Error("Error al cargar el carrito");

        const carrito = await res.json();
        renderizarCarrito(carrito, container);

    } catch (err) {
        container.innerHTML = `<p style="color:#FF3B3B">Error: ${err.message}</p>`;
    }
}

function renderizarCarrito(carrito, container) {
    if (!carrito.items || carrito.items.length === 0) {
        container.innerHTML = `
            <div class="carrito-vacio">
                <h3 style="color:#BFBFBF">Tu carrito está vacío</h3>
                <a href="/static/productos.html"><button class="btn" style="margin-top:1rem">Ir a Productos</button></a>
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="carrito-container">
            ${carrito.items.map(item => `
                <div class="carrito-item">
                    <div class="carrito-item-info">
                        <h4>${item.nombre}</h4>
                        <p>Cantidad: ${item.cantidad}</p>
                    </div>
                    <div class="carrito-item-precio">$${item.precio.toLocaleString()}</div>
                    <div class="carrito-item-subtotal">$${item.subtotal.toLocaleString()}</div>
                    <div>
                        <button class="btn btn-small btn-secondary" onclick="actualizarItemCarrito(${item.id}, ${item.cantidad - 1})" ${item.cantidad <= 1 ? 'disabled' : ''}>-</button>
                        <span style="margin: 0 0.5rem; color:#FFFFFF">${item.cantidad}</span>
                        <button class="btn btn-small btn-secondary" onclick="actualizarItemCarrito(${item.id}, ${item.cantidad + 1})">+</button>
                        <button class="btn btn-small" style="margin-left:0.5rem; background:#FF3B3B" onclick="eliminarItemCarrito(${item.id})">Eliminar</button>
                    </div>
                </div>
            `).join("")}
            <div class="carrito-total">
                Total: $${carrito.total.toLocaleString()}
            </div>
            <div style="text-align:right; margin-top:1rem">
                <button class="btn" style="width:auto" onclick="vaciarCarrito()">Vaciar Carrito</button>
            </div>
        </div>
    `;
}

async function actualizarItemCarrito(itemId, nuevaCantidad) {
    if (nuevaCantidad < 1) return;

    const token = sessionStorage.getItem("token");
    try {
        const res = await fetch(`${API}/carrito/${itemId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ cantidad: nuevaCantidad })
        });

        if (res.ok) {
            verCarrito();
            actualizarCartCount();
        } else {
            const data = await res.json();
            alert(`Error: ${data.detail}`);
        }
    } catch (err) {
        alert("Error de conexión");
    }
}

async function eliminarItemCarrito(itemId) {
    if (!confirm("¿Eliminar este producto del carrito?")) return;

    const token = sessionStorage.getItem("token");
    try {
        const res = await fetch(`${API}/carrito/${itemId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.ok) {
            verCarrito();
            actualizarCartCount();
        } else {
            alert("Error al eliminar producto");
        }
    } catch (err) {
        alert("Error de conexión");
    }
}

async function vaciarCarrito() {
    if (!confirm("¿Vaciar todo el carrito?")) return;

    const token = sessionStorage.getItem("token");
    try {
        const res = await fetch(`${API}/carrito/`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.ok) {
            verCarrito();
            actualizarCartCount();
        } else {
            alert("Error al vaciar carrito");
        }
    } catch (err) {
        alert("Error de conexión");
    }
}

async function actualizarCartCount() {
    const token = sessionStorage.getItem("token");
    if (!token) return;

    try {
        const res = await fetch(`${API}/carrito/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (res.ok) {
            const carrito = await res.json();
            const count = carrito.items ? carrito.items.reduce((sum, item) => sum + item.cantidad, 0) : 0;
            const cartCountEl = document.getElementById("cartCount");
            if (cartCountEl) {
                cartCountEl.textContent = count;
                cartCountEl.style.display = count > 0 ? "flex" : "none";
            }
        }
    } catch (err) {
        console.error("Error actualizando contador de carrito");
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

function guardarSesionPagina() {
    const path = window.location.pathname;
    if (!path.includes("index.html") && path !== "/") {
        sessionStorage.setItem("sesion_pagina", path);
    }
}

function cerrarSesion() {
    if (!confirm("¿Cerrar sesión?")) return;
    sessionStorage.clear();
    window.location.href = "/";
}

// ─────────────────────────────────────────
// SESIÓN
// ─────────────────────────────────────────
const usuario = sessionStorage.getItem("usuario");
if (usuario) {
    inicializarRoles();
    guardarSesionPagina();
    actualizarCartCount();
}

// Redirigir si ya hay sesión en login
if (window.location.pathname === "/" || window.location.pathname === "/static/index.html") {
    if (sessionStorage.getItem("token")) {
        window.location.href = "/static/home.html";
    }
}

// Cargar productos si estamos en productos.html
if (window.location.pathname.includes("productos.html")) {
    cargarCategoriasFiltro();
}

// Cargar carrito si estamos en carrito.html
if (window.location.pathname.includes("carrito.html")) {
    if (!sessionStorage.getItem("token")) {
        window.location.href = "/";
    } else {
        verCarrito();
    }
}

// Verificar admin si estamos en admin.html
if (window.location.pathname.includes("admin.html")) {
    verificarAdmin();
}

// ─────────────────────────────────────────
// ADMIN FUNCTIONS
// ─────────────────────────────────────────
async function verificarAdmin() {
    const token = sessionStorage.getItem("token");
    const rol = sessionStorage.getItem("rol");

    if (!token || rol !== "admin") {
        alert("Acceso restringido. Solo administradores.");
        window.location.href = "/";
        return;
    }

    inicializarRoles();
    await cargarCategoriasAdmin();
    await cargarCategoriasList();
    await cargarProductosList();
}

async function crearProducto() {
    const token = sessionStorage.getItem("token");
    if (!token) { window.location.href = "/"; return; }

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
        setTimeout(() => { cargarProductosList(); limpiarFormProducto(); }, 1000);
    } catch (err) {
        mostrarAlerta("alertError", "Error de conexión");
    }
}

async function crearCategoria() {
    const token = sessionStorage.getItem("token");
    if (!token) { window.location.href = "/"; return; }

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
            container.innerHTML = "<p style='color:#BFBFBF'>No hay categorías.</p>";
            return;
        }

        container.innerHTML = categorias.map(c => `
            <div style="padding:0.5rem; border-bottom:1px solid #0B0B0B">
                <strong style="color:#FFFFFF">${c.nombre}</strong>
                <span style="color:#BFBFBF"> - ${c.descripcion || "Sin descripción"}</span>
            </div>
        `).join("");
    } catch (err) {
        console.error("Error cargando categorías");
    }
}

async function cargarProductosList() {
    try {
        const res = await fetch(`${API}/productos/`);
        const productos = await res.json();
        const container = document.getElementById("productosList");
        if (!container) return;

        if (productos.length === 0) {
            container.innerHTML = "<p style='color:#BFBFBF'>No hay productos.</p>";
            return;
        }

        container.innerHTML = productos.map(p => `
            <div style="padding:0.5rem; border-bottom:1px solid #0B0B0B; display:flex; justify-content:space-between; align-items:center">
                <div>
                    <strong style="color:#FFFFFF">${p.nombre}</strong>
                    <span style="color:#FF3B3B"> - $${p.precio}</span>
                    <span style="color:#BFBFBF"> | Stock: ${p.stock}</span>
                </div>
                <button class="btn btn-small" style="background:#FF3B3B" onclick="eliminarProducto(${p.id})">Eliminar</button>
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
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (!res.ok) { alert("Error al eliminar producto"); return; }
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

async function cargarCategoriasAdmin() {
    try {
        const res = await fetch(`${API}/categorias/`);
        const categorias = await res.json();
        const select = document.getElementById("categoria_id");
        if (!select) return;

        select.innerHTML = `<option value="">Sin categoría</option>`;
        categorias.forEach(c => {
            select.innerHTML += `<option value="${c.id}">${c.nombre}</option>`;
        });
    } catch (err) {
        console.error("Error cargando categorías para el select");
    }
}
