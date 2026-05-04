// ✅ API ya está definida en app.js - No duplicar

// Asegurar que las funciones estén disponibles en el scope global
window.cargarTarjetas = async function() {
    try {
        if (typeof API === 'undefined') {
            console.error("❌ API no está definida");
            return;
        }
        
        const token = sessionStorage.getItem("token");
        if (!token) {
            console.log("No hay sesión activa");
            return;
        }

        const res = await fetch(`${API}/tarjeta/mis-tarjetas`, {
            headers: { 
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            console.error("Error al cargar tarjetas:", res.status);
            return;
        }

        const tarjetas = await res.json();
        window.mostrarTarjetas(tarjetas);
    } catch (error) {
        console.error("Error al cargar tarjetas:", error);
    }
};

// --- MOSTRAR TARJETAS EN PANTALLA ---
window.mostrarTarjetas = function(tarjetas) {
    const contenedor = document.getElementById('tarjetas-list');
    if (!contenedor) return;

    if (tarjetas.length === 0) {
        contenedor.innerHTML = '<p style="color: #BFBFBF;">No hay tarjetas registradas</p>';
        return;
    }

    let html = '<div class="row">';
    tarjetas.forEach(tarjeta => {
        const ultimosDigitos = tarjeta.num_tarjeta.slice(-4);
        html += `
            <div class="col-md-4 mb-3">
                <div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 8px;">
                    <h5 class="card-title">${tarjeta.tipo_tarjeta.toUpperCase()}</h5>
                    <p class="card-text" style="font-size: 1.2rem; letter-spacing: 2px;">**** **** **** ${ultimosDigitos}</p>
                    <p class="card-text"><small>Vence: ${tarjeta.fecha_exp}</small></p>
                    <p class="card-text"><strong>Saldo: $${tarjeta.saldo.toFixed(2)}</strong></p>
                    <span class="badge bg-success">${tarjeta.estado_tarjeta}</span>
                </div>
            </div>
        `;
    });
    html += '</div>';
    contenedor.innerHTML = html;
};

// --- VALIDACIÓN DE DATOS ---
window.validarDatos = function() {
    const tipo = document.getElementById('tipo-tarjeta-select')?.value;
    const numero = document.getElementById('numero-tarjeta')?.value;
    const fecha = document.getElementById('fecha-expiracion')?.value;
    const cvv = document.getElementById('codigo-seguridad')?.value;
    const saldo = document.getElementById('saldo')?.value;  // ✅ NUEVO

    return (tipo && numero && fecha && cvv && saldo);  // ✅ NUEVO: Incluir saldo en validación
};

// --- FUNCIÓN REGISTRAR TARJETA ---
window.registrarTarjeta = async function() {
    try {
        console.log("1️⃣ Iniciando registro de tarjeta...");
        
        // Verificar si hay token
        const token = sessionStorage.getItem("token");
        console.log("2️⃣ Token:", token ? "✅ Encontrado" : "❌ NO ENCONTRADO");
        
        if (!token) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Debes iniciar sesión para registrar una tarjeta',
                confirmButtonColor: '#FF3B3B'
            });
            return;
        }

        if (!window.validarDatos()) {
            console.log("3️⃣ Validación fallida - Datos incompletos");
            Swal.fire({
                icon: 'warning',
                title: 'Datos incompletos',
                text: 'Por favor, rellena todos los campos del formulario.',
                confirmButtonColor: '#FF3B3B'
            });
            return;
        }

        console.log("3️⃣ Validación exitosa");

        // Obtener valores
        const payload = {
            tipo_tarjeta: document.getElementById('tipo-tarjeta-select').value,
            numero_tarjeta: document.getElementById('numero-tarjeta').value.replace(/-/g, ''),
            fecha_expiracion: document.getElementById('fecha-expiracion').value,
            codigo_seguridad: document.getElementById('codigo-seguridad').value,
            saldo: parseFloat(document.getElementById('saldo').value)  // ✅ NUEVO: Incluir saldo
        };

        console.log("4️⃣ Payload:", payload);

        Swal.fire({ title: 'Registrando...', didOpen: () => Swal.showLoading() });

        const res = await fetch(`${API}/tarjeta/registro`, {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        console.log("5️⃣ Respuesta del servidor:", res.status);

        const data = await res.json();
        console.log("6️⃣ Datos de respuesta:", data);

        if (!res.ok) {
            throw new Error(data.detail || data.message || "Error al registrar la tarjeta");
        }

        console.log("7️⃣ ¡Tarjeta registrada exitosamente!");

        Swal.fire({
            icon: 'success',
            title: '¡Éxito!',
            text: 'Tarjeta registrada correctamente',
            confirmButtonColor: '#FF3B3B'
        }).then(() => {
            // Limpiar formulario
            document.getElementById('numero-tarjeta').value = '';
            document.getElementById('fecha-expiracion').value = '';
            document.getElementById('codigo-seguridad').value = '';
            document.getElementById('saldo').value = '';  // ✅ NUEVO: Limpiar saldo
            // Recargar tarjetas
            window.cargarTarjetas();
            // Cerrar el formulario
            const collapseBtn = document.getElementById('collapseExample');
            if (collapseBtn) {
                const bsCollapse = new bootstrap.Collapse(collapseBtn, { toggle: true });
            }
        });

    } catch (error) {
        console.error("❌ Fallo en el registro:", error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: error.message,
            confirmButtonColor: '#FF3B3B'
        });
    }
};

// Esperamos a que el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ DOM listo - Inicializando tarjeta.js");
    
    // Cargar tarjetas al abrir la página
    window.cargarTarjetas();
    
    // --- FORMATEO DE NÚMERO DE TARJETA ---
    const inputTarjeta = document.getElementById('numero-tarjeta');
    if (inputTarjeta) {
        inputTarjeta.addEventListener('input', (e) => {
            let valor = e.target.value.replace(/\D/g, '');
            let groups = valor.match(/.{1,4}/g);
            if (groups) {
                e.target.value = groups.join('-').substring(0, 19);
            } else {
                e.target.value = valor.substring(0, 19);
            }
        });
    }

    // --- FORMATEO DE FECHA ---
    const inputFecha = document.getElementById('fecha-expiracion');
    if (inputFecha) {
        inputFecha.addEventListener('input', (e) => {
            let valor = e.target.value.replace(/\D/g, '');
            if (valor.length >= 2) {
                valor = valor.substring(0, 2) + '/' + valor.substring(2, 4);
            }
            e.target.value = valor;
        });

        inputFecha.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && inputFecha.value.length === 3) {
                inputFecha.value = inputFecha.value.substring(0, 2);
            }
        });
    }
});