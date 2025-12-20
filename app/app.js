const state = {
  series: [],
  chart: null,
};

const sampleUrl = 'data/sample_metrics.json';

function formatNumber(value, digits = 1) {
  return Number.parseFloat(value).toFixed(digits).replace(/\.0+$/, '.0');
}

function computeSeriesMetrics(point) {
  const durable = point.mu_a * point.q;
  const returnWork = point.mu_a - durable;
  const cEff = Math.max(0, (point.capacity ?? 0) - (point.drift ?? 0));
  const bound = point.b_req ? cEff / point.b_req : 0;
  const exceedance = Math.max(0, (point.drift ?? 0) + point.lambda * (point.b_req ?? 0) - (point.capacity ?? 0));

  return {
    ...point,
    mu_d: durable,
    return_work: returnWork,
    c_eff: cEff,
    mu_bar: bound,
    exceedance,
  };
}

function updateSummaryFromInputs() {
  const capacity = Number.parseFloat(document.getElementById('capacity').value) || 0;
  const drift = Number.parseFloat(document.getElementById('drift').value) || 0;
  const bReq = Number.parseFloat(document.getElementById('breq').value) || 1;
  const attempted = Number.parseFloat(document.getElementById('attempted').value) || 0;
  const durability = Number.parseFloat(document.getElementById('durability').value) || 0;
  const lambda = Number.parseFloat(document.getElementById('lambda').value) || 0;

  const cEff = Math.max(0, capacity - drift);
  const bound = bReq > 0 ? cEff / bReq : 0;
  const muD = attempted * durability;
  const returnWork = attempted - muD;
  const exceedance = Math.max(0, drift + lambda * bReq - capacity);

  document.getElementById('capacityOut').textContent = `${formatNumber(cEff, 1)}`;
  document.getElementById('boundOut').textContent = `${formatNumber(bound, 1)}`;
  document.getElementById('durableOut').textContent = `${formatNumber(muD, 1)}`;
  document.getElementById('returnOut').textContent = `${formatNumber(returnWork, 1)}`;
  document.getElementById('exceedanceOut').textContent = `${formatNumber(exceedance, 1)}`;

  const checklist = document.getElementById('checklist');
  if (!checklist.dataset.dynamic) {
    const liveItem = document.createElement('li');
    liveItem.id = 'liveStatus';
    checklist.appendChild(liveItem);
    checklist.dataset.dynamic = 'true';
  }

  const live = document.getElementById('liveStatus');
  if (muD > bound && bound > 0) {
    live.innerHTML = `<strong>Status:</strong> Durable settlement exceeds the declared frontier — definitions or inputs likely mismatch.`;
    live.style.color = '#f87171';
  } else if (attempted > bound && muD < attempted) {
    live.innerHTML = `<strong>Status:</strong> Forcing throughput beyond μ̄_d; expect rising ρ_gen and tail thickening.`;
    live.style.color = '#fbbf24';
  } else {
    live.innerHTML = `<strong>Status:</strong> Within capacity. Track Z(t) and tails to confirm durability.`;
    live.style.color = '#5eead4';
  }
}

function renderChart(series) {
  const ctx = document.getElementById('flowChart');
  const labels = series.map((p) => p.week);
  const muD = series.map((p) => p.mu_d);
  const muA = series.map((p) => p.mu_a);
  const lambda = series.map((p) => p.lambda);
  const backlog = series.map((p) => p.backlog);

  const data = {
    labels,
    datasets: [
      {
        label: 'μ_d(t;T) durable',
        data: muD,
        borderColor: '#5eead4',
        backgroundColor: 'rgba(94, 234, 212, 0.1)',
        tension: 0.35,
        fill: false,
        yAxisID: 'y',
      },
      {
        label: 'μ_a(t) attempts',
        data: muA,
        borderColor: '#7dd3fc',
        backgroundColor: 'rgba(125, 211, 252, 0.1)',
        tension: 0.35,
        fill: false,
        yAxisID: 'y',
      },
      {
        label: 'λ(t) initiation',
        data: lambda,
        borderColor: '#c084fc',
        backgroundColor: 'rgba(192, 132, 252, 0.1)',
        tension: 0.35,
        fill: false,
        yAxisID: 'y',
      },
      {
        label: 'L(t) backlog',
        data: backlog,
        borderColor: '#f3b07c',
        backgroundColor: 'rgba(243, 176, 124, 0.15)',
        tension: 0.15,
        fill: true,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        title: { display: true, text: 'Rates (per period)', color: '#b4b8c7' },
        grid: { color: 'rgba(255,255,255,0.04)' },
        ticks: { color: '#b4b8c7' },
      },
      y1: {
        position: 'right',
        title: { display: true, text: 'Visible unresolved L(t)', color: '#b4b8c7' },
        grid: { drawOnChartArea: false },
        ticks: { color: '#b4b8c7' },
      },
      x: {
        ticks: { color: '#b4b8c7', maxRotation: 0 },
        grid: { color: 'rgba(255,255,255,0.04)' },
      },
    },
    plugins: {
      legend: {
        labels: { color: '#eef2ff' },
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.dataset.label}: ${formatNumber(context.parsed.y, 1)}`,
        },
      },
    },
  };

  if (state.chart) {
    state.chart.data = data;
    state.chart.options = options;
    state.chart.update();
  } else {
    state.chart = new Chart(ctx, {
      type: 'line',
      data,
      options,
    });
  }
}

async function loadSampleData() {
  try {
    const response = await fetch(sampleUrl);
    const payload = await response.json();
    const annotatedSeries = payload.series.map((point) => {
      const enriched = computeSeriesMetrics({
        lambda: point.lambda,
        mu_a: point.mu_a,
        q: point.q,
        backlog: point.backlog,
        week: point.week,
        drift: point.drift,
        b_req: point.b_req,
        capacity: point.capacity,
      });
      return enriched;
    });

    state.series = annotatedSeries;

    document.getElementById('boundaryName').value = payload.boundary || 'Declared boundary';
    document.getElementById('horizon').value = payload.horizon_days || 30;
    document.getElementById('fidelity').value = payload.fidelity || '';

    const latest = annotatedSeries[annotatedSeries.length - 1];
    document.getElementById('capacity').value = latest.capacity ?? 0;
    document.getElementById('drift').value = latest.drift ?? 0;
    document.getElementById('breq').value = latest.b_req ?? 1;
    document.getElementById('attempted').value = latest.mu_a ?? 0;
    document.getElementById('durability').value = latest.q ?? 0;
    document.getElementById('lambda').value = latest.lambda ?? 0;

    renderChart(annotatedSeries);
    updateSummaryFromInputs();
  } catch (err) {
    console.error('Failed to load sample data', err);
  }
}

function bootstrap() {
  document.getElementById('loadSample').addEventListener('click', loadSampleData);
  document.getElementById('recalc').addEventListener('click', updateSummaryFromInputs);
  loadSampleData();
}

document.addEventListener('DOMContentLoaded', bootstrap);
