console.log("Hello world")
console.log("Hello world")
console.log("Hello world")
console.log("Hello world")

// Get the searchField element by its ID


// Get the search field element by its ID
const searchField = document.getElementById("searchField");

// Add event listener for 'input' event
searchField.addEventListener('input', (e) => {
  const searchValue = e.target.value.trim(); // Get and trim the value

  if (searchValue.length > 0) {
    console.log(searchValue); // Print the search value to the console

    // Make the API call
    fetch("/search-expense", {
      body: JSON.stringify({searchText: searchValue }),  // Send search term as body
      method: "POST",  // Use POST method
    })
    .then((res) => res.json())  // Parse response as JSON
    .then((data) => {
      console.log(data);  // Print the data from the server to the console
    });
  }
});




// const searchField = document.querySelector("#searchField");
// const tableOutput = document.querySelector(".table-output");
// const appTable = document.querySelector(".app-table");
// const paginationContainer = document.querySelector(".pagination-container");
// tableOutput.style.display = "none";


// tableOutput.style.display="none";


// searchField.addEventListener('keyup', (e)=>{
//   const searchValue=e.target.value;
//   if(searchValue.trim().length>0){
//     //console.log(searchValue);


//     fetch("/search-expense", {
//       body: JSON.stringify({searchText:searchValue}),
//       method: "POST"
//     })
//     .then((res)=>res.json())
//     .then((data) =>{
//       //console.log("data", data);
//       appTable.style.display = "none";
//       tableOutput.style.display = "block";
      
//       if(data.length===0){
//         console.log("No matching results found");
//         console.log("data", data);

//         tableOutput.innerHTML="No Matching results";

//       }
      
//     });
//   }

// });
