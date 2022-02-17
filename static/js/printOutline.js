console.log("printOutline.js");

let printOut = function (event) {
  console.log("printOutline.js printOut");
  let outline_btns = document.getElementsByClassName(
    "student-outline-head-buttons"
  )[0];
  outline_btns.style.display = "none";
  let bottom_nav = document.getElementById("bottom-nav");
  bottom_nav.style.display = "none";
  let action_btns = document.getElementsByClassName("outline-action");
  for (let i = 0; i < action_btns.length; i++) {
    action_btns[i].style.display = "none";
  }
  let delete_btn = document.getElementById("delete-stud");
  delete_btn.style.display = "none";
  //   document.body.style.width = "110%";
  window.print();
  location.reload();
};



// Print Defaulters notice
let printNotices = function (event) {
  console.log("printNotices")
  top_nav = document.getElementById("nav");
  top_nav.style.display = "none";
  let bottom_nav = document.getElementById("bottom-nav");
  bottom_nav.style.display = "none";
  let defaulters_head = document.getElementsByClassName("defaulters-notice-head")[0];
  defaulters_head.style.display = "none";
  window.print();
  location.reload();
}