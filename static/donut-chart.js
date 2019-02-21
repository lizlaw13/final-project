// do not resize the chart canvas when its container does (keep at 600x400px)
Chart.defaults.global.responsive = false;
// define the chart data
let chartData = {
    labels: JSON.parse(document.querySelector('#myDoughnutChart').dataset.labels),
    datasets: [{
        label: 'Total Mood Count',
        data: JSON.parse(document.querySelector('#myDoughnutChart').dataset.data),
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
    }]
}

// get chart canvas
var ctx = document.getElementById("myDoughnutChart").getContext("2d");


// create the chart using the chart canvas
var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
    options: {
        title: {
            display: true,
        }
    }
});



