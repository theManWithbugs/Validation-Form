anychart.onDocumentReady(function () {
    fetch('/faixas-etarias/')
        .then(response => response.json())
        .then(data => {
            var chartData = {
                title: 'Faixas Etarias de idades (Porcentagem)',
                header: ['#', 'Acre'],
                rows: data.faixas_etarias
            };

            var chart = anychart.column();
            chart.data(chartData);
            chart.animation(true);
            chart.yAxis().labels().format('{%Value}{groupsSeparator: }');
            chart.yAxis().title('Indice');
            chart.labels().enabled(true).position('center-top').anchor('center-bottom').format('{%Value}{groupsSeparator: }%');
            chart.hovered().labels(false);
            chart.legend().enabled(true).fontSize(13).padding([0, 0, 20, 0]);
            chart.interactivity().hoverMode('single');
            chart.tooltip().positionMode('point').position('center-top').anchor('center-bottom').offsetX(0).offsetY(5)
                .titleFormat('{%X}').format('{%SeriesName} : #{%Value}{groupsSeparator: }');

            // Definindo as cores das colunas
            var colors = ['#00008B'];
            var series = chart.getSeriesAt(0);
            series.fill(colors);

            chart.container('grafico');
            chart.draw();
        })
        .catch(error => console.error('Erro ao carregar os dados:', error));
});