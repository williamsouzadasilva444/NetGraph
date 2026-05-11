const API = 'http://localhost:5000';

document.querySelector('#btn-scan').addEventListener('click', async () => {
    // 1. Escaneia a rede
    const resScan = await fetch(`${API}/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target: '192.168.1.0/24' })
    });
    const dadosScan = await resScan.json();

    // 2. Constrói o grafo com Tarjan
    const resGrafo = await fetch(`${API}/build-graph`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dadosScan)
    });
    const dadosGrafo = await resGrafo.json();

    // 3. Exibe o grafo gerado pelo pyvis dentro do front-end
    document.querySelector('#canvas').innerHTML =
        `<iframe src="${API}${dadosGrafo.grafo_url}"
                 width="100%" height="600px"
                 style="border:none;">
         </iframe>`;

    // 4. Exibe pontos críticos
    console.log('Bridges encontradas:', dadosGrafo.bridges);
});

document.querySelector('#btn-export').addEventListener('click', () => {
    window.open(`${API}/export`);
});