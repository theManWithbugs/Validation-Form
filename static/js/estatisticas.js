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
    anychart.onDocumentReady(function () {
        const genderData = [
            { name: 'Masculino', value: data.porcentagem_masculino },
            { name: 'Feminino', value: data.porcentagem_feminino }
        ];

        // Criação do gráfico de pizza 3D para gênero
        const genderChart = anychart.pie3d(genderData);
        genderChart.title('Porcentagens de Gênero');
        genderChart.labels().enabled(true).format('{%Value}{groupsSeparator: }%');
        genderChart.container('container_gender_chart');
        genderChart.draw();
    });
}

window.onload = fetchHistoricos;

anychart.onDocumentReady(function () {
	// set chart theme
anychart.theme('lightBlue');
      // create column chart
      var chart = anychart.column3d();

      // turn on chart animation
      chart.animation(true);

      // set chart title text settings
      chart.title('Top 10 Cosmetic Products by Revenue');

      // create area series with passed data
      chart.column([
        ['Rouge', '80540'],
        ['Foundation', '94190'],
        ['Mascara', '102610'],
        ['Lip gloss', '110430'],
        ['Lipstick', '128000'],
        ['Nail polish', '143760'],
        ['Eyebrow pencil', '170670'],
        ['Eyeliner', '213210'],
        ['Eyeshadows', '249980']
      ]);

      chart
        .tooltip()
        .position('center-top')
        .anchor('center-bottom')
        .offsetX(0)
        .offsetY(5)
        .format('${%Value}');

      // set scale minimum
      chart.yScale().minimum(0);

      // set yAxis labels formatter
      chart.yAxis().labels().format('{%Value}{groupsSeparator: }');

      chart.tooltip().positionMode('point');
      chart.interactivity().hoverMode('by-x');

      chart.xAxis().title('Products by Revenue');
      chart.yAxis().title('Revenue in Dollars');

      // set container id for the chart
      chart.container('container_col');

      // initiate chart drawing
      chart.draw();
    });