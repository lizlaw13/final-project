// Global parameters:
// do not resize the chart canvas when its container does (keep at 600x400px)
Chart.Legend.prototype.afterFit = function() {
  this.height = this.height + 50;
};
Chart.defaults.global.responsive = false;

// define the chart data
let chartData = {
  labels: JSON.parse(document.querySelector("#myChart").dataset.labels),
  datasets: [
    {
      label: document.querySelector("#myChart").dataset.label,
      fill: true,
      lineTension: 0.1,
      backgroundColor: "rgba(151,249,190,0.5)",
      borderColor: "rgba(173,216,230)",
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: "miter",
      pointBorderColor: "rgba(0,0,0)",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(173,216,230)",
      pointHoverBorderColor: "rgba(173,216,230)",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: JSON.parse(document.querySelector("#myChart").dataset.data),
      spanGaps: false
    }
  ]
};

// get chart canvas
var ctx = document.getElementById("myChart").getContext("2d");

// create the chart using the chart canvas
var myChart = new Chart(ctx, {
  type: "line",
  data: chartData,
  options: {
    scales: {
      yAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Mood (Scale 1- 5)"
            // labels: JSON.parse(document.querySelector('#myChart').dataset.labels),
          }
        }
      ],
      xAxes: [
        {
          type: "time",
          distribution: "linear",
          time: {
            unit: "day",
            displayFormats: {
              day: "MMM D"
            }
          },
          scaleLabel: {
            display: true,
            labelString: "Date"
          }
        }
      ]
    }
  }
});
$("#chart-legend").html(myChart.generateLegend());
