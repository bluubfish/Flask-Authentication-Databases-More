
// take noteId and send post request to /delete-note endpoint
// after get response from endpoint, gna reload the window/refresh page
function deleteNote(noteId) {
    console.log("entered JS")
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }