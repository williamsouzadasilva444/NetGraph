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

// ─────────────────────────────────────────
// Botão: Scan the Network (scan + build graph)
// ─────────────────────────────────────────
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

        if (!scanData.nodes?.length)
            throw new Error('Nenhum host encontrado na rede.');

        canvasMsg('🕸️', `${scanData.nodes.length} hosts encontrados`, 'Construindo o grafo...');

        // 2. Constrói o grafo
        const resGrafo = await fetch(`${API}/build-graph`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(scanData)
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


// ─────────────────────────────────────────
// Botão: Show Graph Details
// Painel completo para administradores de rede
// ─────────────────────────────────────────
document.querySelector('#btn-details').addEventListener('click', () => {
    if (!graphData || !scanData) {
        canvasMsg('ℹ️', 'Nenhum dado disponível', 'Execute "Scan the Network" primeiro.');
        return;
    }

    // Nível de risco baseado na quantidade de bridges
    const totalBridges = graphData.bridges?.length ?? 0;
    const nivelRisco = totalBridges === 0
        ? { label: 'BAIXO', color: '#22d3ee', icon: '🟢' }
        : totalBridges <= 2
            ? { label: 'MÉDIO', color: '#f59e0b', icon: '🟡' }
            : { label: 'ALTO', color: '#ef4444', icon: '🔴' };

    // Lista de bridges
    const bridgesHtml = totalBridges > 0
        ? graphData.bridges.map(b => `
            <div style="
                display:flex; align-items:center; gap:0.8rem;
                padding:0.6rem 1rem;
                background:rgba(239,68,68,0.08);
                border:1px solid rgba(239,68,68,0.25);
                border-left:3px solid #ef4444;
                border-radius:8px;
                font-size:0.85rem;
            ">
                <span>⚠️</span>
                <div>
                    <span style="color:#ef4444; font-weight:600">${b.from}</span>
                    <span style="color:#9ca3af"> ↔ </span>
                    <span style="color:#ef4444; font-weight:600">${b.to}</span>
                    <br>
                    <span style="color:#9ca3af; font-size:0.78rem">
                        Remoção desta conexão isola parte da rede
                    </span>
                </div>
            </div>`).join('')
        : `<div style="
                padding:0.6rem 1rem;
                background:rgba(34,211,238,0.08);
                border:1px solid rgba(34,211,238,0.2);
                border-left:3px solid #22d3ee;
                border-radius:8px;
                color:#22d3ee;
                font-size:0.85rem;
           ">✅ Nenhuma bridge crítica encontrada — rede com redundância adequada</div>`;

    // Lista de hosts
    const hostsHtml = scanData.nodes.map(node => `
        <div style="
            display:flex; align-items:center; gap:0.8rem;
            padding:0.5rem 0.8rem;
            background:rgba(255,255,255,0.02);
            border:1px solid rgba(255,255,255,0.06);
            border-radius:8px;
            font-size:0.82rem;
        ">
            <span style="color:#6366F1; font-size:1rem">🖥️</span>
            <div style="flex:1">
                <span style="color:#f3f4f6; font-weight:600">${node.id}</span>
                <span style="color:#9ca3af; margin-left:0.5rem; font-size:0.78rem">${node.vendor || 'Vendor desconhecido'}</span><br>
                <span style="color:#6366F1; font-size:0.75rem">MAC: ${node.mac || 'N/A'}</span>
            </div>
            <span style="
                font-size:0.7rem; padding:0.2rem 0.5rem;
                background:rgba(34,211,238,0.1);
                color:#22d3ee; border-radius:4px;
            ">UP</span>
        </div>`).join('');

    document.querySelector('#canvas').innerHTML = `
        <div style="
            padding:1.5rem; height:100%;
            overflow-y:auto; font-family:inherit;
            color:#f3f4f6; line-height:1.6;
        ">
            <!-- Cabeçalho -->
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1.5rem;">
                <h2 style="color:#6366F1; font-size:1.1rem; margin:0">📊 Análise da Rede</h2>
                <span style="
                    font-size:0.75rem; padding:0.3rem 0.8rem;
                    background:rgba(99,102,241,0.15);
                    border:1px solid rgba(99,102,241,0.3);
                    border-radius:20px; color:#a5b4fc;
                ">${new Date().toLocaleString('pt-BR')}</span>
            </div>

            <!-- Cards de resumo -->
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:0.8rem; margin-bottom:1.5rem;">
                <div style="
                    padding:1rem; text-align:center;
                    background:rgba(99,102,241,0.08);
                    border:1px solid rgba(99,102,241,0.2);
                    border-radius:10px;
                ">
                    <div style="font-size:1.4rem; font-weight:700; color:#6366F1">${graphData.total_nodes}</div>
                    <div style="font-size:0.75rem; color:#9ca3af">Nós na rede</div>
                </div>
                <div style="
                    padding:1rem; text-align:center;
                    background:rgba(34,211,238,0.08);
                    border:1px solid rgba(34,211,238,0.2);
                    border-radius:10px;
                ">
                    <div style="font-size:1.4rem; font-weight:700; color:#22d3ee">${graphData.total_edges}</div>
                    <div style="font-size:0.75rem; color:#9ca3af">Conexões</div>
                </div>
                <div style="
                    padding:1rem; text-align:center;
                    background:rgba(${totalBridges > 0 ? '239,68,68' : '34,211,238'},0.08);
                    border:1px solid rgba(${totalBridges > 0 ? '239,68,68' : '34,211,238'},0.2);
                    border-radius:10px;
                ">
                    <div style="font-size:1.4rem; font-weight:700; color:${totalBridges > 0 ? '#ef4444' : '#22d3ee'}">${totalBridges}</div>
                    <div style="font-size:0.75rem; color:#9ca3af">Bridges críticas</div>
                </div>
            </div>

            <!-- Nível de risco -->
            <div style="
                display:flex; align-items:center; gap:1rem;
                padding:0.8rem 1.2rem; margin-bottom:1.5rem;
                background:rgba(${nivelRisco.color === '#ef4444' ? '239,68,68' : nivelRisco.color === '#f59e0b' ? '245,158,11' : '34,211,238'},0.08);
                border:1px solid ${nivelRisco.color}40;
                border-radius:10px;
            ">
                <span style="font-size:1.3rem">${nivelRisco.icon}</span>
                <div>
                    <span style="color:#9ca3af; font-size:0.8rem">Nível de risco estrutural: </span>
                    <strong style="color:${nivelRisco.color}">${nivelRisco.label}</strong>
                    <br>
                    <span style="color:#9ca3af; font-size:0.75rem">
                        ${totalBridges === 0
            ? 'A rede possui caminhos alternativos — boa resiliência'
            : `${totalBridges} ponto(s) sem redundância — falha pode isolar segmentos`}
                    </span>
                </div>
            </div>

            <!-- Bridges / Pontos críticos -->
            <div style="margin-bottom:1.5rem;">
                <h3 style="
                    color:#ef4444; font-size:0.85rem; font-weight:600;
                    margin-bottom:0.7rem; text-transform:uppercase; letter-spacing:0.05em;
                ">⚠️ Pontos Críticos — Bridges</h3>
                <div style="display:flex; flex-direction:column; gap:0.5rem;">
                    ${bridgesHtml}
                </div>
            </div>

            <!-- Legenda do grafo -->
            <div style="margin-bottom:1.5rem;">
                <h3 style="
                    color:#9ca3af; font-size:0.85rem; font-weight:600;
                    margin-bottom:0.7rem; text-transform:uppercase; letter-spacing:0.05em;
                ">🎨 Legenda do Grafo</h3>
                <div style="display:flex; flex-direction:column; gap:0.4rem; font-size:0.82rem;">
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="width:12px;height:12px;border-radius:50%;background:#6366F1;display:inline-block"></span>
                        <span style="color:#9ca3af">Gateway / Roteador — hub central da rede</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="width:12px;height:12px;border-radius:50%;background:#22d3ee;display:inline-block"></span>
                        <span style="color:#9ca3af">Host ativo — dispositivo comum</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="width:28px;height:3px;background:#ef4444;display:inline-block;border-radius:2px"></span>
                        <span style="color:#9ca3af">Aresta vermelha — bridge (conexão crítica)</span>
                    </div>
                    <div style="display:flex; align-items:center; gap:0.6rem;">
                        <span style="width:28px;height:2px;background:rgba(255,255,255,0.25);display:inline-block;border-radius:2px"></span>
                        <span style="color:#9ca3af">Aresta branca — conexão normal</span>
                    </div>
                </div>
            </div>

            <!-- Hosts descobertos -->
            <div>
                <h3 style="
                    color:#9ca3af; font-size:0.85rem; font-weight:600;
                    margin-bottom:0.7rem; text-transform:uppercase; letter-spacing:0.05em;
                ">🖧 Hosts Descobertos (${scanData.nodes.length})</h3>
                <div style="display:flex; flex-direction:column; gap:0.4rem;">
                    ${hostsHtml}
                </div>
            </div>

        </div>`;
});


// ─────────────────────────────────────────
// Botão: Save and Export
// ─────────────────────────────────────────
document.querySelector('#btn-export').addEventListener('click', () => {
    if (!graphData) {
        canvasMsg('ℹ️', 'Nada para exportar', 'Execute "Scan the Network" primeiro.');
        return;
    }
    window.open(`${API}/export`);
});