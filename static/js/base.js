anychart.onDocumentReady(function () {
    fetch('/faixas-etarias/')
        .then(response => response.json())
        .then(data => {
            // Verifique se os dados têm a estrutura correta
            if (!data.faixas_etarias || !Array.isArray(data.faixas_etarias)) {
                throw new Error('Dados inválidos recebidos.');
            }

            var chart = anychart.column(); // Inicializa o gráfico de colunas
            chart.animation(true);
            chart.yAxis().labels().format('{%Value}{groupsSeparator: }');
            chart.yAxis().title('Porcentagem');
            chart.labels().enabled(true).position('center-top').anchor('center-bottom').format('{%Value}{groupsSeparator: }%');
            chart.hovered().labels(false);
            chart.legend().enabled(true).fontSize(13).padding([0, 0, 20, 0]);
            chart.interactivity().hoverMode('single');
            chart.tooltip().positionMode('point').position('center-top').anchor('center-bottom').offsetX(0).offsetY(5)
                .titleFormat('{%X}').format('{%SeriesName} : #{%Value}{groupsSeparator: }');

            // Defina uma lista de cores para as colunas
            const colors = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#8E44AD', '#3498DB', '#E67E22'];

            // Adiciona cada faixa etária como uma série única
            data.faixas_etarias.forEach((faixa, index) => {
                const series = chart.column([{ x: faixa[0], value: faixa[1] }]); // Cria uma nova série
                series.fill(colors[index % colors.length]); // Aplica uma cor diferente para cada série
                series.name(faixa[0]); // Define o nome da série como a faixa etária
            });

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


