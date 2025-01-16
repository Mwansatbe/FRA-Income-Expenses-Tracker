// console.log("hello world")

// console.log("Hello")

// const ctx = document.getElementById('myChart');

// new Chart(ctx, {
//   type: 'doughnut',
//   data: {
//     labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//     datasets: [{
//       label: '# of Votes',
//       data: [12, 19, 3, 5, 2, 3],
//       backgroundColor: [
//         'rgba(255, 99, 132, 0.2)', // Red
//         'rgba(54, 162, 235, 0.2)', // Blue
//         'rgba(255, 206, 86, 0.2)', // Yellow
//         'rgba(75, 192, 192, 0.2)', // Green
//         'rgba(153, 102, 255, 0.2)', // Purple
//         'rgba(255, 159, 64, 0.2)'  // Orange
//       ],
//       borderColor: [
//         'rgba(255, 99, 132, 1)',   // Red
//         'rgba(54, 162, 235, 1)',   // Blue
//         'rgba(255, 206, 86, 1)',   // Yellow
//         'rgba(75, 192, 192, 1)',   // Green
//         'rgba(153, 102, 255, 1)',  // Purple
//         'rgba(255, 159, 64, 1)'    // Orange
//       ],
//       borderWidth: 1
//     }]
//   },
//   options: {
//    title:{
//      display:true,
//     text:'Expenses per Category'
//    }
   
//   }
// });

const renderChart = (data, labels) => {
  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Last 6 months income',
        data: data,
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
      title: {
        display: true,
        text: 'Income per Source'
      }
    }
  });
};

const getChartData = () => {
  fetch('/income/income_sources_summary')
    .then((res) => res.json())
    .then((results) => {
      console.log("Results", results);
      const source_data = results.income_source_data;
      const [labels, data] = [Object.keys(source_data), Object.values(source_data)];
      renderChart(data, labels);
    });
};

document.addEventListener('DOMContentLoaded', () => {
  getChartData();
});





