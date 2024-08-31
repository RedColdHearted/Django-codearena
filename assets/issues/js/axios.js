// This file handle a issue solve page reload functionality through long pulling
// that wait creating TestCaseResult instances for solution

// Getting a variables from the page dataset
const documentData = document.currentScript.dataset;
const startFetch = ( documentData.start_fetch === "true")
const url = documentData.url

// Performs axios requests to endpoint of list TestCaseResult by solution id
function checkSolutionStatus() {
  axios.get(url)
    .then(response => {
          // Checking if response contains data from request
      if (response.data.results) {
        location.reload();
      }
    })
    .catch(error => {
      console.error("Error: ", error);
    });
}

// Long pool every 5 sec if template context doesn't contain TestCaseResults
if (startFetch){
  setInterval(checkSolutionStatus, 5000);
}
