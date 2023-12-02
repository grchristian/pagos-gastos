// Definición de colores para las gráficas
var colors = [
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

function fetchAndPlotData(url, plotFunction) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => plotFunction(data));
}

function plotGastosEstatus(data) {
  var gastosEstatusLabels = Object.keys(data);
  var gastosEstatusValues = Object.values(data);

  var gastosEstatusData = {
    x: gastosEstatusLabels,
    y: gastosEstatusValues,
    type: "bar",
    marker: {
      color: colors.slice(0, gastosEstatusLabels.length),
    },
  };

  var layout = {
    title: "Estatus de Gastos",
    barmode: "group",
  };

  Plotly.newPlot("gastos-grafico-1", [gastosEstatusData], layout);
}

function plotGastosMontos(data) {
  var gastosMontosLabels = data.nombres_gastos;
  var gastosMontosValues = data.montos_gastos;

  var gastosMontosData = {
    x: gastosMontosLabels,
    y: gastosMontosValues,
    type: "bar",
    marker: {
      color: colors.slice(0, gastosMontosLabels.length),
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
}

function plotPagosEstatus(data) {
  var pagosEstatusLabels = Object.keys(data);
  var pagosEstatusValues = Object.values(data);

  var pagosEstatusData = {
    labels: pagosEstatusLabels,
    values: pagosEstatusValues,
    type: "pie",
    textinfo: "label+percent",
    insidetextorientation: "radial",
    marker: {
      colors: colors.slice(0, pagosEstatusLabels.length),
    },
  };
  console.log(pagosEstatusData);
  var layout = {
    title: "Distribución de Estados de Pagos",
  };

  Plotly.newPlot("pagos-grafico-1", [pagosEstatusData], layout);
}

function plotPagosTotales(data) {
  var traces = [];
  var colorIndex = 0;

  for (var cuenta in data) {
    var trace = {
      x: data[cuenta].fechas,
      y: data[cuenta].totales,
      type: "scatter",
      mode: "lines+markers",
      name: cuenta,
      marker: {
        color: colors[colorIndex % colors.length],
      },
    };
    traces.push(trace);
    colorIndex++;
  }

  var layout = {
    title: "Total de Pagos por Cuenta Bancaria a lo Largo del Tiempo",
    xaxis: {
      title: "Fecha",
    },
    yaxis: {
      title: "Total Pagado",
    },
  };
  Plotly.newPlot("pagos-grafico-2", traces, layout);
}

function plotCuentasDisponibilidad(data) {
  var trace = {
    x: data.map((cuenta) => cuenta.nombre),
    y: data.map((cuenta) => cuenta.disponible),
    mode: "markers",
    marker: {
      size: data.map((cuenta) => cuenta.disponible),
      sizeref:
        (2.0 * Math.max(...data.map((cuenta) => cuenta.disponible))) / 100 ** 2,
      sizemode: "area",
      color: colors.slice(0, data.length),
    },
    text: data.map((cuenta) => cuenta.nombre),
  };

  var layout = {
    title: "Disponibilidad en Cuentas Bancarias",
    xaxis: {
      title: "Cuenta Bancaria",
    },
    yaxis: {
      title: "Cantidad Disponible",
    },
  };

  Plotly.newPlot("cuentas-grafico-1", [trace], layout);
}

function plotPagosEstadisticas(data) {
  var trace1 = {
    x: data.meses,
    y: data.totales,
    type: "scatter",
    mode: "lines+markers",
    name: "Total",
    line: { color: "blue" },
  };

  var trace2 = {
    x: data.meses,
    y: data.promedios,
    type: "scatter",
    mode: "lines+markers",
    name: "Promedio",
    line: { color: "green" },
  };

  var layout = {
    title: "Estadísticas de Pagos por Mes",
    xaxis: {
      title: "Mes",
    },
    yaxis: {
      title: "Cantidad",
    },
  };

  Plotly.newPlot("pagos-grafico-3", [trace1, trace2], layout);
}

function plotGastosPorCuenta(data) {
  var traces = [];
  var colorIndex = 0;

  for (var cuenta in data) {
    var trace = {
      x: data[cuenta].meses,
      y: data[cuenta].totales,
      type: "scatter",
      mode: "lines+markers",
      name: cuenta,
      line: { color: colors[colorIndex % colors.length] },
    };
    traces.push(trace);

    // Agregar la línea de tendencia
    var traceTendencia = {
      x: data[cuenta].meses,
      y: data[cuenta].tendencia,
      type: "scatter",
      mode: "lines",
      name: cuenta + " Tendencia",
      line: { color: colors[colorIndex % colors.length], dash: "dot" },
    };
    traces.push(traceTendencia);

    colorIndex++;
  }

  var layout = {
    title: "Tendencia de Gastos por Cuenta Bancaria",
    xaxis: { title: "Mes" },
    yaxis: { title: "Total Gastado" },
  };

  Plotly.newPlot("cuentas-grafico-2", traces, layout);
}

document.addEventListener("DOMContentLoaded", function () {
  fetchAndPlotData("/api/gastos-estatus", plotGastosEstatus);
  fetchAndPlotData("/api/gastos-montos", plotGastosMontos);
  fetchAndPlotData("/api/pagos-estatus", plotPagosEstatus);
  fetchAndPlotData("/api/pagos-totales", plotPagosTotales);
  fetchAndPlotData("/api/cuentas-disponibilidad", plotCuentasDisponibilidad);
  fetchAndPlotData("/api/pagos-estadisticas", plotPagosEstadisticas);
  fetchAndPlotData("/api/gastos-por-cuenta", plotGastosPorCuenta);
});
