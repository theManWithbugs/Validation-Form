anychart.onDocumentReady(function () {
    fetch('/faixas-etarias/')
        .then(response => response.json())
        .then(data => {
            // Verifique se os dados têm a estrutura correta
            if (!data.faixas_etarias || !Array.isArray(data.faixas_etarias)) {
                throw new Error('Dados inválidos recebidos.');
            }

            var chartData = {
                title: 'Faixas Etárias de Idades (Porcentagem Ativos)',
                header: ['Faixa Etária', 'Porcentagem'],
                rows: data.faixas_etarias
            };

            var chart = anychart.column();
            chart.data(chartData);
            chart.animation(true);
            chart.yAxis().labels().format('{%Value}{groupsSeparator: }');
            chart.yAxis().title('Índice');
            chart.labels().enabled(true).position('center-top').anchor('center-bottom').format('{%Value}{groupsSeparator: }%');
            chart.hovered().labels(false);
            chart.legend().enabled(true).fontSize(13).padding([0, 0, 20, 0]);
            chart.interactivity().hoverMode('single');
            chart.tooltip().positionMode('point').position('center-top').anchor('center-bottom').offsetX(0).offsetY(5)
                .titleFormat('{%X}').format('{%SeriesName} : #{%Value}{groupsSeparator: }');

            // Ajustando a cor da série
            var series = chart.column(data.faixas_etarias);
            series.fill('#000000'); // Preto sólido

            chart.background().fill('rgba(255, 255, 255, 0.8)'); 

            chart.container('grafico');
            chart.draw();
        })
        .catch(error => console.error('Erro ao carregar os dados:', error));
});

const botoes = document.querySelectorAll('.botao');

botoes.forEach(botao => {
    botao.addEventListener('mouseover', () => {
        botao.classList.add('hover');
    });

    botao.addEventListener('mouseout', () => {
        botao.classList.remove('hover');
    });
});

document.getElementById('confirmBtn').addEventListener('click', function() {
    var myModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    myModal.show();
});

document.getElementById('finalizeRemoval').addEventListener('click', function() {
    document.getElementById('myform').submit();
});


