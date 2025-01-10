// console.log("Hello world")
// console.log("Hello world")
// console.log("Hello world")
// console.log("Hello world")


document.getElementById("searchField").addEventListener("input", (e) => {
  const searchValue = e.target.value;

  // Get the pagination container and the shown-pages div
  const paginationContainer = document.querySelector(".pagination");
  const shownPages = document.querySelector(".shown-pages");

  // If search input has any value
  if (searchValue.length > 0) {
    console.log(searchValue); // Print the search value to the console

    // Hide the pagination container and shown-pages div while searching
    if (paginationContainer) {
      paginationContainer.style.display = "none";
    }
    if (shownPages) {
      shownPages.style.display = "none";
    }

    // Make the API call to search expenses
    fetch("/income/search-income", {
      body: JSON.stringify({ searchText: searchValue }), // Send search term as body
      method: "POST", // Use POST method
    })
    .then((res) => res.json())  // Parse response as JSON
    .then((data) => {
      // Get the table body
      const tableBody = document.querySelector("tbody");

      // Clear existing rows in the table body
      tableBody.innerHTML = '';

      if (data.length > 0) {
        // Loop through the data and create a row for each result
        data.forEach(item => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${item.amount}</td>
            <td>${item.source}</td>
            <td>${item.description}</td>
            <td>${item.date}</td>
            <td><a href="/income/edit-income/${item.id}" class="btn btn-secondary btn-sm">Edit</a></td>
          `;
          tableBody.appendChild(row);
        });
      } else {
        // If no results, display "No matching results"
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="5" class="text-center">No matching results found</td>`;
        tableBody.appendChild(row);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  } else {
    // If search field is empty, reload the page to restore the default table (all expenses)
    location.reload();  // This will reload the page to display the default table

    // Ensure that the pagination and shown-pages are shown again after reload
    if (paginationContainer) {
      paginationContainer.style.display = "block";
    }
    if (shownPages) {
      shownPages.style.display = "block";
    }
  }
});

