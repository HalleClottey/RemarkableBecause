const note_div = document.querySelector('#note_div')

// Start the process of asking the server for the current note once a timer
// expires.
function startTimer() {
  const microseconds = 2000  // 2 seconds
  window.setTimeout(fetchCurrentNote, microseconds)
}

// Ask the server for the current note immediately.
function fetchCurrentNote() {
  fetch('/ajax/get_current_node')
    .then(function(response) {
      return response.json()
    })
    .then(function (myJson) {
      // Update the div.
      note_div.innerHTML = myJson.note

      // Start the timer again for the next request.
      startTimer()
    })
}

if (note_div != null) {
  // If note_div is null it means that the user is not logged in.  This is
  // because the jinja template for the '/' handler only renders this div
  // when the user is logged in.  Querying for a node that does not exist
  // returns null.

  // Start by fetching the current note without any delay.
  fetchCurrentNote()
}
