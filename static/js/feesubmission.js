console.log("feesubmission.js");

window.onload = function () {
  let fee_detail_input = document.getElementsByClassName("fee-detail-input")[0];
  fee_detail_input.childNodes[1].focus();
};

let addCheque = function (event) {
  console.log("addCheque");
  let cheque_details_div =
    document.getElementsByClassName("fee-cheque-details")[0];
  cheque_details_div.style.display = "block";
  cheque_details_div.childNodes[1].focus();
  let fee_mop = document.getElementById("fee-mop");
  fee_mop.value = "Cheque";
  alert(
    "Now, MOP changes to 'Cheque'! Please fill the details. To cancel, please refresh the page."
  );
};

let addOnlinePay = function (event) {
  console.log("addOnlinePay");
  let online_details_div = document.getElementsByClassName("online-pay")[0];
  online_details_div.style.display = "block";
  online_details_div.childNodes[1].focus();
  let fee_mop = document.getElementById("fee-mop");
  fee_mop.value = "Online/NEFT";
  alert(
    "Now, MOP changes to 'Online/NEFT'! Please fill the details. To cancel, please refresh the page."
  );
};

// add miscellanneous fees
let addMisc = function (event) {
  console.log("addMisc");
  let misc_details_div = document.getElementsByClassName("misc-fee")[0];
  misc_details_div.style.display = "block";
  let fee_form = document.getElementsByTagName("form")[0];
  fee_form.action = "/fee/misc/";
};

let plusMisc = function (event) {
  console.log("plusMisc");
  let misc_elements = document.getElementById("misc-fees");
  let misc_elements_html = misc_elements.innerHTML;
  // misc_elements.innerHTML +=

  let add_misc_element = `<div class="fee-cheque-details misc-fee minus-more-misc" style="display: block;">
  <i class="fas fa-minus-circle" onclick="minusMisc(event)"></i>
  <select name="misc-type" id="miscellaneous-type">
    <option value="None" selected>Select Miscellaneous</option>
    <option value="Admission Fee">Admission Fee</option>
    <option value="Registration Fee">Registration Fee</option>
    <option value="Late Fee">Late Fee</option>
    <option value="Fine">Fine</option>
    <option value="Other">Other</option>
  </select>
  <input type="number" name="misc-amount" placeholder="Amount:" />
  <input type="text" name="misc-reason" placeholder="Reason:" />
  <i class="fas fa-plus-circle add-more-misc" onclick="plusMisc(event)"></i>
</div>`;
  misc_elements.innerHTML = add_misc_element + misc_elements_html;
};

let minusMisc = function (event) {
  console.log("minusMisc");
  let misc_element = document.getElementsByClassName("misc-fee");
  console.log(misc_element.length);
  let parent_div = event.target.parentNode;
  parent_div.parentNode.removeChild(parent_div);
  if (misc_element.length === 0) {
    // let fee_form = document.getElementsByTagName("form")[0];
    // fee_form.action = "/fee/submit/";
    location.reload();
  }
};

let embedStudentInfo = function (data) {
  console.log("embedStudentInfo");
  let stud_add_no = document.getElementById("stud-add-no");
  stud_add_no.innerHTML = data.add_no;
  console.log(data.add_no);
  let stud_name = document.getElementById("stud-name");
  stud_name.innerHTML = data.name;
  let father_name = document.getElementById("stud-father-name");
  father_name.innerHTML = data.father_name;
  let stud_class = document.getElementById("stud-class");
  stud_class.innerHTML = data.class;
  let stud_total_session_fee = document.getElementById(
    "stud-total-session-fee"
  );
  stud_total_session_fee.innerHTML = `&#8377;${data.total_session_fee}.00/-`;
  let session_fee_submitted = document.getElementById("stud-fee-submitted");
  session_fee_submitted.innerHTML = `&#8377;${data.session_fee_submitted}.00/-`;
  // console.log(data.session_fee_submitted);
  let session_fee_left = document.getElementById("stud-fee-left");
  session_fee_left.innerHTML = `&#8377;${data.session_fee_left}.00/-`;
};

let requestStudentInfo = function (add_no) {
  console.log("requestStudentInfo");
  axios({
    method: "get",
    url: "/fee/api/student_details/?add_no=" + add_no,
  })
    .then((response) => embedStudentInfo(response.data))
    .catch((error) => console.log(error));
};

let keyPress = function (event) {
  // console.log("keyPress");
  console.log("key up");
  console.log(event.target.value);
  let fee_detail_input = document.getElementsByClassName("fee-detail-input")[0];
  // fee_detail_input.childNodes[3].focus();
  // console.log(fee_detail_input.childNodes);
  requestStudentInfo(event.target.value);
  // if (event.keyCode === 13) {
  //   console.log("hits enter");
  //   console.log(event.target.value);
  //   let fee_detail_input =
  //     document.getElementsByClassName("fee-detail-input")[0];
  //   fee_detail_input.childNodes[3].focus();
  //   // console.log(fee_detail_input.childNodes);
  //   requestStudentInfo(event.target.value);
  // }
};

// window.onbeforeunload = function () {
//   console.log("onbeforeunload");
//   alert("Please fill the details. To cancel, please refresh the page.");
// }

// window.onunload = function () {
//   console.log("onunload");
//   alert("Please fill the details. To cancel, please refresh the page.");
// }

// window.onbeforeunload = function() {
//   console.log("onbeforeunload");
//   // check for all empty fields
//   let fee_detail_input = document.querySelectorAll(".fee-detail-input input");
//   let fee_detail_input_array = Array.from(fee_detail_input);
//   for (let i = 0; i < fee_detail_input_array.length; i++) {
//     if (fee_detail_input_array[i].value === "") {
//       return "Please fill the details. To cancel, please refresh the page.";
//     }
//   }
//   // let inputs = document.getElementsByTagName("input");
//   // for (let i = 0; i < inputs.length; i++) {
//   //   if (inputs[i].value === "") {
//   //     return "Please fill the details. To cancel, please refresh the page.";
//   //   }
//   // }

//   // return "Please fill the details. To cancel, please refresh the page.";
//   // return "Do you really want to leave our brilliant application?";
//   //if we return nothing here (just calling return;) then there will be no pop-up question at all
//   return;
// };
