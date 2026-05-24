 // código desenvolvido com auxilia de Inteligência Artificial (IA) - Claude para aprendizado
// e aplicação prática de conceitos de redes e grafos.

const API = 'http://localhost:5000';

// Estado global
let scanData = null;
let graphData = null;


// Helpers de UI

function setBtnLoading(id, loading, label) {
    const btn = document.querySelector(id);
    btn.disabled = loading;
    btn.textContent = loading ? 'Aguarde...' : label;
    btn.style.opacity = loading ? '0.55' : '1';
}

function canvasMsg(icon, title, detail = '', color = '#6366F1') {
    document.querySelector('#canvas').innerHTML = `
        <div style="
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; height:100%; gap:0.6rem;
            font-family:inherit; text-align:center; padding:2rem;
        ">
            <span style="font-size:2.2rem">${icon}</span>
            <strong style="color:${color};font-size:1rem">${title}</strong>
            <span style="color:#9ca3af;font-size:0.85rem">${detail}</span>
        </div>`;
}

// Botão: Scan the Network (scan + build graph)

document.querySelector('#btn-scan').addEventListener('click', async () => {
    setBtnLoading('#btn-scan', true, 'Scan the Network');
    canvasMsg('🔍', 'Escaneando a rede...', 'Descobrindo hosts ativos');

    try {
        // 1. Escaneia a rede
        const resScan = await fetch(`${API}/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });

        if (!resScan.ok) throw new Error(`Erro no scan: HTTP ${resScan.status}`);
        scanData = await resScan.json();

        if (scanData.erro) throw new Error(scanData.erro);
        if (!scanData.nodes?.length) throw new Error('Nenhum host encontrado na rede.');

        canvasMsg('🕸️', `${scanData.nodes.length} hosts encontrados`, 'Construindo o grafo...');

        // 2. Constrói o grafo (scanner já rodou, build usa lista_adjacente internamente)
        
        const resGrafo = await fetch(`${API}/build-graph`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });

        if (!resGrafo.ok) throw new Error(`Erro ao construir grafo: HTTP ${resGrafo.status}`);
        graphData = await resGrafo.json();

        if (graphData.erro) throw new Error(graphData.erro);

        // 3. Exibe o grafo no canvas
        document.querySelector('#canvas').innerHTML =
            `<iframe src="${API}${graphData.grafo_url}"
                     width="100%" height="100%"
                     style="border:none; background:transparent; display:block;">
             </iframe>`;

        console.log('✅ Grafo gerado:', graphData);
        console.log('🔴 Bridges:', graphData.bridges);

    } catch (err) {
        console.error(err);
        canvasMsg('⚠️', 'Erro', err.message, '#ef4444');
    } finally {
        setBtnLoading('#btn-scan', false, 'Scan the Network');
    }
});

// funcao para exibir detalhes do grafo no html
function fillPanel(details) {
    // obtendo id de cada campo
    const deviceList = document.getElementById("device-list");

    const articulations = document.getElementById("articulation-points");

    const bridges = document.getElementById("bridges");

    const centrality = document.getElementById("centrality");

    // limpando cada campo dos detalhes
    deviceList.innerHTML = "";
    articulations.innerHTML = "";
    bridges.innerHTML = "";
    centrality.innerHTML = "";

    // exibindo cada dispositivo
    for (const ip of details.ips) {
        const li = document.createElement("li");

        li.textContent = ip;

        deviceList.appendChild(li);
    };

    // exibindo cada ponto de articulacao
    for (const ip of details.articulacoes) {
        const li = document.createElement("li");

        li.textContent = ip;

        articulations.appendChild(li);
    };

    // exibindo cada ponte
    for (const ponte of details.pontes) {
        const li = document.createElement("li");

        li.textContent = `${ponte[0]} ↔ ${ponte[1]}`;

        bridges.appendChild(li);
    };

    // exibindo no central
    centrality.textContent = details.central;
}

// funcao para resgatar detalhes do grafo
async function loadDetails() {
    try {
        const answer = await fetch("/network-details");
    
        const details = await answer.json();

        fillPanel(details)

    } catch(erro) {
        console.error(erro);
    }
}

// mostrar detalhes do grafo
const showBtn = document.getElementById("btn-details");

const closeBtn = document.getElementById("close-panel-btn");

const panel = document.getElementById("network-details-panel");

// metodo para exibir detalhes no botao btn-details
showBtn.addEventListener("click", async() => {
    await loadDetails();

    panel.classList.remove("hidden");
});

// fechar detalhes ao clicar no botao close-panel-btn
closeBtn.addEventListener("click", () => {
    panel.classList.add("hidden");
});
