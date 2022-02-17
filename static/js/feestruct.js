axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
console.log("feestruct.js");

let okUpdateHandler = function (res, fee_id) {
  console.log("okUpdateHandler");
  console.log(res);
  location.reload();
};

let okHandler = function (event, fee_id) {
  console.log("okHandler");
  console.log("fee id", fee_id);
  let fee_name = document.getElementById(`fee-name#${fee_id}`).value;
  console.log("fee name", fee_name);
  let fee_amount = document.getElementById(`fee-amount#${fee_id}`).value;
  console.log("fee amount", fee_amount);

  axios({
    method: "patch",
    url: "/fee/structUpdate/",
    data: {
      fee_struct_id: fee_id,
      fee_name: fee_name,
      fee_amount: fee_amount,
    },
  })
    .then((res) => okUpdateHandler(res, fee_id))
    .catch((err) => console.log(err));
};

let createFeeStruct = function (name_value, amount_value, fee_id) {
  return `<div class="menu-list tech-exam-list add-fee-input">
      <input type="text" id="fee-name#${fee_id}" placeholder="Fee Name" value="${name_value}" />
      <input type="number" id="fee-amount#${fee_id}" placeholder="Fee Amount (in Rupees)" value="${amount_value}" />
      <input type="hidden" value="${fee_id}" />
      <div>
        <button onclick="okHandler(event, ${fee_id})" class="btn">OK</button>
        <button type="reset" class="btn" onclick="javascript:location.reload()">Cancel</button>
      </div>
  </div>`;
};

let okHandlerNew = function (event) {
  console.log("okHandlerNew");
  let fee_name = document.getElementById("fee-name-new").value;
  console.log("fee name", fee_name);
  let fee_amount = document.getElementById("fee-amount-new").value;
  console.log("fee amount", fee_amount);
  // console.log(window.location.href);
  let url = window.location.href;
  let url_split = url.split("/");
  // console.log(url_split);
  console.log(url_split[url_split.length - 2]);

  axios({
    method: "post",
    url: "http://127.0.0.1:8000/fee/structUpdate/",
    data: {
      fee_name: fee_name,
      fee_amount: fee_amount,
      class_id: url_split[url_split.length - 2],
      month_id: url_split[url_split.length - 1],
    },
  })
    .then((res) => {
      console.log(res);
      location.reload();
    })
    .catch((err) => console.log(err));
};

let createFeeStructNew = function () {
  return `<div class="menu-list tech-exam-list add-fee-input">
      <input type="text" id="fee-name-new" placeholder="Fee Name" />
      <input type="number" id="fee-amount-new" placeholder="Fee Amount (in Rupees)" />
      <div>
        <button onclick="okHandlerNew(event)" class="btn">OK</button>
        <button type="reset" class="btn" onclick="javascript:location.reload()">Cancel</button>
      </div>
  </div>`;
};

let addFee = function (event) {
  console.log("addFee");
  let main_fee_struct = document.getElementById("main-fee-struct");
  console.log(main_fee_struct);
  main_fee_struct.innerHTML += createFeeStructNew("", "");
  let add_fee_input = document.getElementsByClassName("add-fee-input")[0];
  add_fee_input.childNodes[1].focus();
};

let editFee = function (event, fee_id) {
  console.log("editFee");
  // console.log(event.target.parentNode.parentNode.parentNode);
  let fee_elem = event.target.parentNode.parentNode.parentNode;
  console.log(fee_elem);
  var fee_elem_outerhtml = fee_elem.outerHTML;
  let fee_name =
    event.target.parentNode.parentNode.parentNode.childNodes[3].childNodes[1]
      .childNodes[1].innerText;
  console.log(fee_name);
  let fee_amount =
    event.target.parentNode.parentNode.parentNode.childNodes[3].childNodes[3]
      .childNodes[1].innerText;
  console.log(fee_amount);
  fee_elem.outerHTML = createFeeStruct(
    fee_name,
    fee_amount,
    fee_id,
    fee_elem_outerhtml
  );
  let add_fee_input = document.getElementsByClassName("add-fee-input")[0];
  add_fee_input.childNodes[1].focus();
  // console.log(add_fee_input.childNodes[1]);
};

// delete fee structure
let deleteFee = function (event, fee_id) {
  console.log("deleteFee");
  console.log(fee_id);

  axios({
    method: "delete",
    url: "http://127.0.0.1:8000/fee/structUpdate/",
    data: {
      fee_struct_id: fee_id,
    },
  })
    .then((res) => {
      console.log(res);
      location.reload();
    })
    .catch((err) => console.log(err));
};
