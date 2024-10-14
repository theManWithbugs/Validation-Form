// Função para buscar os dados
async function fetchHistoricos() {
    const response = await fetch('/api/historicos/');
    const data = await response.json();

    // Criação do gráfico de pizza com dados dos tipos penais
    anychart.onDocumentReady(function () {
        // Criação dos dados do gráfico a partir das porcentagens
        const chartData = data.tipos_penais_porcentagens.map(([tipo, porcentagem]) => {
            return { name: tipo, value: porcentagem.toFixed(2) }; // Formata para duas casas decimais
        });

        // Criação do gráfico de pizza 3D
        var chart = anychart.pie3d(chartData);

        // Configurações do gráfico
        chart.title('Porcentagens dos Tipos Penais');
        chart.labels().enabled(true).format('{%Value}{groupsSeparator: }%');

        // Configurando o container do gráfico
        chart.container('container_chart');
        chart.draw();
    });
}

window.onload = fetchHistoricos;

