// dashboard-charts.js

function initDashboardCharts() {
  // Definir colores para cada barra
  var barColors = [
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
    "rgba(255, 206, 86, 0.6)",
    "rgba(75, 192, 192, 0.6)",
    "rgba(153, 102, 255, 0.6)",
    "rgba(255, 159, 64, 0.6)",
    "rgba(255, 99, 132, 0.6)",
    "rgba(34, 177, 76, 0.6)",
    "rgba(255, 206, 86, 0.6)",
    "rgba(0, 162, 232, 0.6)",
    "rgba(153, 102, 255, 0.6)",
    "rgba(255, 159, 105, 0.6)",
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
  ];

  // gastos-grafico-1
  var gastosEstatusData = {
    x: gastosEstatusLabels,
    y: gastosEstatusValues,
    type: "bar",
    marker: {
      color: barColors.slice(0, gastosEstatusLabels.length),
    },
  };

  var layout = {
    title: "Estatus de Gastos",
    barmode: "group",
  };

  Plotly.newPlot("gastos-grafico-1", [gastosEstatusData], layout);

  // # gastos-grafico-2
  var gastosMontosData = {
    x: gastosMontosLabels,
    y: gastosMontosValues,
    type: "bar",
    marker: {
      color: barColors.slice(0, gastosMontosLabels.length),
    },
    name: "Cantidad",
  };

  var layout = {
    title: "Gastos por Cantidad",
    barmode: "group",
    xaxis: {
      tickangle: -45,
      showticklabels: false,
      title: "Gastos",
    },
    yaxis: {
      title: "",
    },
    showlegend: false,
  };

  Plotly.newPlot("gastos-grafico-2", [gastosMontosData], layout);

  // Otros gráfic
}

document.addEventListener("DOMContentLoaded", initDashboardCharts);
