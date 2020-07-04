var TITLE = 'Temperature Data';

var X_AXIS = 'Time';  // x-axis label and label in tooltip
var Y_AXIS = 'Temperature (deg F)'; // y-axis label and label in tooltip

var BEGIN_AT_ZERO = false;  // Should x-axis start from 0? `true` or `false`

var SHOW_GRID = true; // `true` to show the grid, `false` to hide
var SHOW_LEGEND = true; // `true` to show the legend, `false` to hide

// https://jsfiddle.net/beaver71/u4wto8z1/
// Modified a function found on jsfiddle to do the opposite
function zeroToNull(array) {
  return array.map(function(v) { 
    if (v==0) return null; else return v;
  });
}

$(document).ready(function() {

  // Read data file and create a chart
  $.get('df1.csv', function(csvString) {

    var data = Papa.parse(csvString).data;
    var timeLabels = data.slice(1).map(function(row) { return row[0]; });

    var datasets = [];
    for (var i = 1; i < data[0].length; i++) {
      datasets.push(
        {
          label: data[0][i], // column name
          data: zeroToNull(data.slice(1).map(function(row) {return row[i]})), // data in that column, and get rid of zeros
          fill: false, // `true` for area charts, `false` for regular line charts
          showLine: false
        }
      )
    }

$().ready(function() {
  $("#T0").html(datasets[0].data.filter(x => x != null).slice(-1)[0]),
  $("#T1").html(datasets[1].data.filter(x => x != null).slice(-1)[0]),
  $("#T2").html(datasets[2].data.filter(x => x != null).slice(-1)[0]),
  $("#T3").html(datasets[3].data.filter(x => x != null).slice(-1)[0]),
  $("#T4").html(datasets[4].data.filter(x => x != null).slice(-1)[0])
});    

//Get start date for the chart
let dateObj = new Date();
dateObj.setDate(dateObj.getDate() - 1);
let myMonth = String(dateObj.getMonth() + 1).padStart(2, '0');
let day = String(dateObj.getDate()).padStart(2, '0');
let year = dateObj.getFullYear();
myDate = year + '-' + myMonth + '-' + day;
    
    // Get container for the chart
    var ctx = document.getElementById('chart-container').getContext('2d');

    new Chart(ctx, {
      type: 'line',

      data: {
        labels: timeLabels,
        datasets: datasets,
      },
      
      options: {
        title: {
          display: true,
          text: TITLE,
          fontSize: 14,
        },
        legend: {
          display: SHOW_LEGEND,
        },
        maintainAspectRatio: false,
        scales: {
          xAxes: [{
            scaleLabel: {
              display: X_AXIS !== '',
              labelString: X_AXIS
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              callback: function(value, index, values) {
                return value.toLocaleString();
              },
            },
            type: 'time',
            display: true,
            time: {
              parser: 'YYYY-MM-DD HH:mm:ss',
              tooltipFormat: 'll HH:mm',
              unit: 'day',
              unitStepSize: 1,
              displayFormats: {'day': 'MM/DD/YYYY'},
              min: myDate,
              //max: '06/10/2020 12:00'
            }
          }],
          yAxes: [{
            beginAtZero: false,
            scaleLabel: {
              display: Y_AXIS !== '',
              labelString: Y_AXIS
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              beginAtZero: BEGIN_AT_ZERO,
	      //steps: 10,
	      //stepValue: 5,
	      max:90,
              callback: function(value, index, values) {
                return value.toLocaleString()
              }
            }
          }]
        },
        tooltips: {
          displayColors: false,
          callbacks: {
            label: function(tooltipItem, all) {
              return all.datasets[tooltipItem.datasetIndex].label
                + ': ' + tooltipItem.yLabel.toLocaleString();
            }
          }
        },
        plugins: {
          colorschemes: {
            scheme: 'brewer.DarkTwo5'
          }
        }
      }
    });

  });

});

