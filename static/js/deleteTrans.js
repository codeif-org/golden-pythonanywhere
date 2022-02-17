axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
console.log("deleteTrans.js");

let updateModels = function (res, fee_id) {
  console.log("updateModels");

  axios({
    method: "get",
    url: "/fee/delete/?id=" + fee_id,
  })
    .then((res) => {
      console.log(res);
      location.reload();
    })
    .catch((err) => console.log(err));
};

let deleteFee = function (event, fee_id, amount, student_id) {
  console.log("deleteFee");
  console.log(fee_id, amount, student_id);
  document.body.style.cursor = "wait";
  document.getElementById("delete-fee-button").disabled = true;
  axios({
    method: "post",
    url: "/fee/submit/",
    data: {
      student: student_id,
      amount: -amount,
      mop: "Delete",
      memo_no: -1,
      submit_date: "2022-1-1",
    },
  })
    .then((res) => updateModels(res, fee_id))
    .catch((err) => console.log(err));
};

// delete student
let deleteStudent = function (event, stud_id) {
  console.log("deleteStudent");
  console.log(stud_id);
  if (
    confirm(
      "Are you sure you want to delete this student? This action cannot be undone and all associated data will be deleted."
    )
  ) {
    axios({
      method: "get",
      url: "/student/delete/?id=" + stud_id,
    })
      .then((res) => {
        console.log(res);
        window.location.href = "/students";
      })
      .catch((err) => console.log(err));
  }
};

// delete misc fee
let deleteMisc = function (event, misc_id) {
  console.log("deleteMisc");
  document.body.style.cursor = "wait";
  document.getElementById("delete-misc-button").disabled = true;
  axios({
    method: "get",
    url: "/fee/misc/delete/?id=" + misc_id,
  })
    .then((res) => {
      console.log(res);
      location.reload();
    })
    .catch((err) => console.log(err));
};
