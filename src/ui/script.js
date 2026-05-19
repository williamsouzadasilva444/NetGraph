// EU CONFESSO QUE EU USEI O CLAUDE PARA ME AJUDAR A ESCREVER ESTE CÓDIGO, MAS EU REVISSEI E TESTEI TUDO MINUCIOSAMENTE. O CLAUDE ME AJUDOU A ORGANIZAR AS IDEIAS E A ESCRITA, MAS AS LÓGICAS DE IMPLEMENTAÇÃO, OS ESTILOS E OS DETALHES FORAM TODOS FEITOS POR MIM. EU QUERO SER TRANSPARENTE SOBRE ISSO, MAS GARANTO QUE O RESULTADO FINAL É UM TRABALHO AUTÊNTICO E DE QUALIDADE.

const API = 'http://localhost:5000';

// Estado global
let scanData = null;
let graphData = null;

// ─────────────────────────────────────────
// Helpers de UI
// ─────────────────────────────────────────
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

function hostCard(node) {
    return `
        <div style="
            padding: 0.7rem 1rem;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            font-size: 0.85rem;
            color: #f3f4f6;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        ">
            <span style="font-size:1.2rem">🖥️</span>
            <div>
                <strong>${node.id}</strong>
                <span style="color:#9ca3af; margin-left:0.5rem">${node.vendor || 'Desconhecido'}</span><br>
                <span style="color:#6366F1; font-size:0.8rem">MAC: ${node.mac || 'N/A'}</span>
            </div>
        </div>`;
}


// ─────────────────────────────────────────
// Botão: Scan the Network
// ─────────────────────────────────────────
document.querySelector('#btn-scan').addEventListener('click', async () => {
    setBtnLoading('#btn-scan', true, 'Scan the Network');
    canvasMsg('🔍', 'Escaneando a rede...', 'Isso pode levar alguns segundos');

    try {
        const res = await fetch(`${API}/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });

        if (!res.ok) throw new Error(`Erro HTTP ${res.status}`);
        scanData = await res.json();

        if (!scanData.nodes?.length)
            throw new Error('Nenhum host encontrado na rede.');

        // Exibe os hosts encontrados no canvas
        document.querySelector('#canvas').innerHTML = `
            <div style="
                padding: 1.5rem; height: 100%;
                overflow-y: auto; font-family: inherit;
            ">
                <p style="color:#6366F1; font-weight:600; margin-bottom:1rem; font-size:0.95rem;">
                    🖧 ${scanData.nodes.length} hosts encontrados — clique em "Build Graph" para visualizar
                </p>
                <div style="display:flex; flex-direction:column; gap:0.6rem;">
                    ${scanData.nodes.map(hostCard).join('')}
                </div>
            </div>`;

    } catch (err) {
        console.error(err);
        canvasMsg('⚠️', 'Erro no scan', err.message, '#ef4444');
    } finally {
        setBtnLoading('#btn-scan', false, 'Scan the Network');
    }
});


// ─────────────────────────────────────────
// Botão: Build Graph
// ─────────────────────────────────────────
document.querySelector('#btn-build').addEventListener('click', async () => {
    if (!scanData?.nodes?.length) {
        canvasMsg('ℹ️', 'Faça o scan primeiro', 'Clique em "Scan the Network" antes de construir o grafo.');
        return;
    }

    setBtnLoading('#btn-build', true, 'Build Graph');
    canvasMsg('🕸️', 'Construindo o grafo...', 'Rodando algoritmo de Tarjan');

    try {
        const res = await fetch(`${API}/build-graph`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(scanData)
        });

        if (!res.ok) throw new Error(`Erro HTTP ${res.status}`);
        graphData = await res.json();

        if (graphData.erro) throw new Error(graphData.erro);

        // Exibe o grafo PyVis no canvas — 100% para preencher o painel
        document.querySelector('#canvas').innerHTML =
            `<iframe src="${API}${graphData.grafo_url}"
                     width="100%" height="100%"
                     style="border:none; background:transparent; display:block;">
             </iframe>`;

        console.log('✅ Grafo gerado:', graphData);
        console.log('🔴 Bridges:', graphData.bridges);

    } catch (err) {
        console.error(err);
        canvasMsg('⚠️', 'Erro ao construir grafo', err.message, '#ef4444');
    } finally {
        setBtnLoading('#btn-build', false, 'Build Graph');
    }
});


// ─────────────────────────────────────────
// Botão: Show Graph Details
// ─────────────────────────────────────────
document.querySelector('#btn-details').addEventListener('click', () => {
    if (!graphData) {
        canvasMsg('ℹ️', 'Nenhum grafo gerado', 'Faça o scan e clique em "Build Graph" primeiro.');
        return;
    }

    const bridgesHtml = graphData.bridges?.length
        ? graphData.bridges.map(b =>
            `<li style="color:#ef4444; margin:0.3rem 0">⚠️ ${b.from} ↔ ${b.to}</li>`
        ).join('')
        : '<li style="color:#22d3ee">✅ Nenhuma bridge crítica encontrada</li>';

    document.querySelector('#canvas').innerHTML = `
        <div style="
            padding:2rem; font-family:inherit; color:#f3f4f6;
            height:100%; overflow-y:auto; line-height:1.9;
        ">
            <h2 style="color:#6366F1; margin-bottom:1.2rem">📊 Detalhes do Grafo</h2>
            <p>🖧 <strong>Hosts encontrados:</strong> ${scanData?.nodes?.length ?? 'N/A'}</p>
            <p>🔵 <strong>Nós no grafo:</strong> ${graphData.total_nodes}</p>
            <p>🔗 <strong>Conexões (arestas):</strong> ${graphData.total_edges}</p>
            <hr style="border-color:rgba(255,255,255,0.1); margin:1rem 0">
            <h3 style="color:#f3f4f6; margin-bottom:0.6rem">🔴 Pontos Críticos (Bridges)</h3>
            <ul style="list-style:none; padding:0">${bridgesHtml}</ul>
        </div>`;
});


// ─────────────────────────────────────────
// Botão: Save and Export
// ─────────────────────────────────────────
document.querySelector('#btn-export').addEventListener('click', () => {
    if (!graphData) {
        canvasMsg('ℹ️', 'Nada para exportar', 'Gere um grafo primeiro.');
        return;
    }
    window.open(`${API}/export`);
});