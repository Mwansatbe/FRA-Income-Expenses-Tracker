console.log("Hello")

const renderChart = (data, labels) => {

  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Last 6 months expenses',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)', // Red
          'rgba(54, 162, 235, 0.2)', // Blue
          'rgba(255, 206, 86, 0.2)', // Yellow
          'rgba(75, 192, 192, 0.2)', // Green
          'rgba(153, 102, 255, 0.2)', // Purple
          'rgba(255, 159, 64, 0.2)'  // Orange
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',   // Red
          'rgba(54, 162, 235, 1)',   // Blue
          'rgba(255, 206, 86, 1)',   // Yellow
          'rgba(75, 192, 192, 1)',   // Green
          'rgba(153, 102, 255, 1)',  // Purple
          'rgba(255, 159, 64, 1)'    // Orange
        ],
        borderWidth: 1
      }]
    },
    options: {
      title: {
        display: true,
        text: 'Expenses per Category'
      }

    }
  });
}


const getChartData = () => {
  fetch('expense_category_summary')
    .then((res) => res.json())
    .then((results) => {
      console.log("Results", results);
      const category_data = results.expense_category_data;
      const [labels, data] = [Object.keys(category_data), Object.values(category_data)];

      renderChart(data, labels);
    });
}

document.onload = getChartData();





