async function carregarReservas() {
    const resp = await fetch("http://127.0.0.1:5000/reservas");
    const reservas = await resp.json();
    const tbody = document.querySelector("#tabelaReservas tbody");
    tbody.innerHTML = "";

    reservas.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${r.id}</td>
            <td>${r.nome_cliente}</td>
            <td>${r.telefone_cliente}</td>
            <td>${r.data}</td>
            <td>${r.hora}</td>
            <td>${r.numero_pessoas}</td>
            <td>${r.status}</td>
            <td>
                <button class="editar-btn">Editar</button>
                <button class="cancelar-btn">Cancelar</button>
            </td>
        `;

        // Adiciona event listeners de forma programática para segurança
        const editarBtn = tr.querySelector(".editar-btn");
        const cancelarBtn = tr.querySelector(".cancelar-btn");

        editarBtn.addEventListener("click", () => abrirModal(r));
        cancelarBtn.addEventListener("click", () => cancelarReserva(r.id));
        
        tbody.appendChild(tr);
    });
}

// Criar nova reserva
document.getElementById("formReserva").addEventListener("submit", async e => {
    e.preventDefault();
    const reserva = {
        nome_cliente: document.getElementById("nome_cliente").value,
        telefone_cliente: document.getElementById("telefone_cliente").value,
        data: document.getElementById("data").value,
        hora: document.getElementById("hora").value + ":00",
        numero_pessoas: parseInt(document.getElementById("numero_pessoas").value)
    };
    const resp = await fetch("http://127.0.0.1:5000/reservas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(reserva)
    });
    const dataResp = await resp.json();
    document.getElementById("mensagem").textContent = dataResp.mensagem;
    carregarReservas();
    e.target.reset();
});

// Abrir modal de edição
function abrirModal(reserva) {
    document.getElementById("modal-edicao").style.display = "block";
    document.getElementById("reserva-id").value = reserva.id;
    document.getElementById("nome_cliente_edit").value = reserva.nome_cliente;
    document.getElementById("telefone_cliente_edit").value = reserva.telefone_cliente;
    document.getElementById("data_edit").value = reserva.data;
    document.getElementById("hora_edit").value = reserva.hora;
    document.getElementById("numero_pessoas_edit").value = reserva.numero_pessoas;
    document.getElementById("status_edit").value = reserva.status;
}

// Fechar modal
function fecharModal() {
    document.getElementById("modal-edicao").style.display = "none";
}

// Salvar edição
async function salvarEdicao() {
    const id = document.getElementById("reserva-id").value;
    const dados = {
        nome_cliente: document.getElementById("nome_cliente_edit").value,
        telefone_cliente: document.getElementById("telefone_cliente_edit").value,
        data: document.getElementById("data_edit").value,
        hora: document.getElementById("hora_edit").value,
        numero_pessoas: parseInt(document.getElementById("numero_pessoas_edit").value),
        status: document.getElementById("status_edit").value
    };
    // **Acento grave (`) corrigido aqui**
    await fetch(`http://127.0.0.1:5000/reservas/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    });
    fecharModal();
    carregarReservas();
}

// Cancelar reserva
async function cancelarReserva(id) {
    if (confirm("Tem certeza que deseja cancelar esta reserva?")) {
        // **Acento grave (`) corrigido aqui**
        await fetch(`http://127.0.0.1:5000/reservas/${id}`, { method: "DELETE"});
        carregarReservas();
    }
}

// Inicializar
carregarReservas();

// Listeners para os botões do modal
document.querySelector("#modal-edicao .modal-conteudo button:first-of-type").addEventListener("click", salvarEdicao);
document.querySelector("#modal-edicao .modal-conteudo button:last-of-type").addEventListener("click", fecharModal);