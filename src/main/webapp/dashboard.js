import { Chart } from 'chart.js';
import axios from 'axios';

const metricsContainer = document.getElementById('metrics-container');
const latencyChart = document.getElementById('latency-chart');
const costChart = document.getElementById('cost-chart');
const errorChart = document.getElementById('error-chart');
const filterInput = document.getElementById('filter-input');
const sortSelect = document.getElementById('sort-select');

let latencyData = [];
let costData = [];
let errorData = [];

axios.get('/api/metrics')
    .then(response => {
        const metrics = response.data;
        metrics.forEach(metric => {
            latencyData.push(metric.latency);
            costData.push(metric.cost);
            errorData.push(metric.errorRate);
        });
        renderCharts();
    })
    .catch(error => console.error(error));

function renderCharts() {
    const latencyCtx = latencyChart.getContext('2d');
    const costCtx = costChart.getContext('2d');
    const errorCtx = errorChart.getContext('2d');

    new Chart(latencyCtx, {
        type: 'line',
        data: {
            labels: Array(latencyData.length).fill().map((_, i) => i),
            datasets: [{
                label: 'Latency',
                data: latencyData,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    new Chart(costCtx, {
        type: 'bar',
        data: {
            labels: Array(costData.length).fill().map((_, i) => i),
            datasets: [{
                label: 'Cost',
                data: costData,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    new Chart(errorCtx, {
        type: 'pie',
        data: {
            labels: Array(errorData.length).fill().map((_, i) => i),
            datasets: [{
                label: 'Error Rates',
                data: errorData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

filterInput.addEventListener('input', () => {
    const filterValue = filterInput.value.toLowerCase();
    const metrics = metricsContainer.children;
    for (let i = 0; i < metrics.length; i++) {
        const metric = metrics[i];
        if (metric.textContent.toLowerCase().includes(filterValue)) {
            metric.style.display = 'block';
        } else {
            metric.style.display = 'none';
        }
    }
});

sortSelect.addEventListener('change', () => {
    const sortValue = sortSelect.value;
    if (sortValue === 'asc') {
        latencyData.sort((a, b) => a - b);
        costData.sort((a, b) => a - b);
        errorData.sort((a, b) => a - b);
    } else if (sortValue === 'desc') {
        latencyData.sort((a, b) => b - a);
        costData.sort((a, b) => b - a);
        errorData.sort((a, b) => b - a);
    }
    renderCharts();
});