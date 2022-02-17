console.log("sessions.js");

let changeSession = function (event) {
  console.log("changeSession");
  let session_id = document.getElementById("change-session-select").value;
  console.log(session_id);
  if (confirm("Do you want to change session?")) {
    axios({
      method: "get",
      url: "/sessions/current-update/?session_id=" + session_id,
    })
      .then((res) => {
        console.log(res);
        location.reload();
      })
      .catch((err) => console.log(err));
  }
};

// add new session
let addSession = function (event) {
  console.log("addSession");
  let session_name = document.getElementById("add-session-input").value;
  console.log(session_name);
  if (confirm("Do you want to add new session?")) {
    if (confirm("Please first read the instructions and then proceed")) {
      axios({
        method: "get",
        url: "/sessions/add-new/?session_name=" + session_name,
      })
        .then((res) => {
          console.log(res);
          location.reload();
        })
        .catch((err) => console.log(err));
    }
  }
};
