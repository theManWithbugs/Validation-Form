async function fetchHistoricos() {
    const response = await fetch('/api/historicos/');
    const data = await response.json();

    anychart.onDocumentReady(function () {

        const chartData = data.tipos_penais_porcentagens.map(([tipo, porcentagem]) => {
            return { name: tipo, value: porcentagem.toFixed(2) }; 
        });

        var chart = anychart.pie3d(chartData);

        chart.title('Porcentagens dos Tipos Penais');
        chart.labels().enabled(true).format('{%Value}{groupsSeparator: }%');

        chart.background().fill('rgba(255, 255, 255, 0.6)'); 

        chart.container('container_chart');
        chart.draw();
    });
}

window.onload = fetchHistoricos;






