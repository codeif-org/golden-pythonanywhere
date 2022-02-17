console.log("reports.js");

let dayWiseReportHandler = function (data, generate_date) {
  console.log("dayWiseReportHandler");
  console.log(data);

  // make report_wait disappear
  let report_wait = document.getElementsByClassName("report-wait")[0];
  report_wait.style.display = "none";

  let generated_report_div = document.getElementById("generated-report-day");
  generated_report_div.style.display = "block";
  let day_report_date_display = document.getElementById(
    "day-report-date-display"
  );
  day_report_date_display.innerHTML = generate_date;
  let day_report_link = document.getElementById("day-report-download-link");
  day_report_link.href = data.file_path;
  console.log("Now you can download the report file");
};

let dayWiseReportRequest = function (generate_date) {
  console.log("dayWiseReportRequest");
  console.log("generate date", generate_date);

  //   make report_wait appear
  let report_wait = document.getElementsByClassName("report-wait")[0];
  report_wait.style.display = "block";

  axios({
    method: "get",
    url: "/reports/api/day/generate/?date=" + generate_date,
  })
    .then((res) => dayWiseReportHandler(res.data, generate_date))
    .catch((err) => console.log(err));
};

let generateRep = function (event) {
  console.log("generateRep");
  let generate_date = document.getElementById(
    "day-wise-report-date-input"
  ).value;
  console.log(generate_date);
  dayWiseReportRequest(generate_date);
};

// date wise report
let dateWiseReportHandler = function (data, start_date, end_date) {
  console.log("dateWiseReportHandler");
  console.log(data);

  // make report_wait disappear
  let report_wait = document.getElementsByClassName("report-wait")[1];
  report_wait.style.display = "none";

  let generated_report_div = document.getElementById("generated-report-date");
  generated_report_div.style.display = "block";
  let date_report_start_date_display = document.getElementById(
    "date-report-start-date-display"
  );
  date_report_start_date_display.innerHTML = start_date;
  let date_report_end_date_display = document.getElementById(
    "date-report-end-date-display"
  );
  date_report_end_date_display.innerHTML = end_date;
  let date_report_link = document.getElementById("date-report-download-link");
  date_report_link.href = data.file_path;
  console.log("Now you can download the report file");
};

let dateWiseReportRequest = function (start_date, end_date) {
  console.log("dateWiseReportRequest");
  console.log(start_date, end_date);

  //   make report_wait appear
  let report_wait = document.getElementsByClassName("report-wait")[1];
  report_wait.style.display = "block";

  console.log(report_wait);
  axios({
    method: "get",
    url:
      "/reports/api/date/generate/?start_date=" +
      start_date +
      "&end_date=" +
      end_date,
  })
    .then((res) => dateWiseReportHandler(res.data, start_date, end_date))
    .catch((err) => console.log(err));
};

let generateDateRep = function (event) {
  console.log("generateDateRep");
  let generate_start_date = document.getElementById(
    "date-wise-report-start-date-input"
  ).value;
  let generate_end_date = document.getElementById(
    "date-wise-report-end-date-input"
  ).value;
  console.log(generate_start_date, generate_end_date);
  dateWiseReportRequest(generate_start_date, generate_end_date);
};



// date wise with details report
let dateWiseWithDReportHandler = function (data, start_date, end_date) {
  console.log("dateWiseWithDReportHandler");
  console.log(data);

  // make report_wait disappear
  let report_wait = document.getElementsByClassName("report-wait")[2];
  report_wait.style.display = "none";

  let generated_report_div = document.getElementById("generated-report-date-with-detail");
  generated_report_div.style.display = "block";
  let date_report_start_date_display = document.getElementById(
    "date-with-detail-report-start-date-display"
  );
  date_report_start_date_display.innerHTML = start_date;
  let date_report_end_date_display = document.getElementById(
    "date-with-detail-report-end-date-display"
  );
  date_report_end_date_display.innerHTML = end_date;
  let date_report_link = document.getElementById("date-with-detail-report-download-link");
  date_report_link.href = data.file_path;
  console.log("Now you can download the report file");
};

let dateWiseWithDReportRequest = function (start_date, end_date) {
  console.log("dateWiseWithDReportRequest");
  console.log(start_date, end_date);

  //   make report_wait appear
  let report_wait = document.getElementsByClassName("report-wait")[2];
  report_wait.style.display = "block";

  console.log(report_wait);
  axios({
    method: "get",
    url:
      "/reports/api/date-with-detail/generate/?start_date=" +
      start_date +
      "&end_date=" +
      end_date,
  })
    .then((res) => dateWiseWithDReportHandler(res.data, start_date, end_date))
    .catch((err) => console.log(err));
};

let generateDateWithDRep = function (event) {
  console.log("generateDateWithDRep");
  let generate_start_date = document.getElementById(
    "date-wise-with-detail-report-start-date-input"
  ).value;
  let generate_end_date = document.getElementById(
    "date-wise-with-detail-report-end-date-input"
  ).value;
  console.log(generate_start_date, generate_end_date);
  dateWiseWithDReportRequest(generate_start_date, generate_end_date);
};




// students cumulative report
let generateStudCumHandler = function (data, class_id) {
  console.log("generateStudCumHandler");
  console.log(data);

  // make report_wait disappear
  let report_wait = document.getElementsByClassName("report-wait")[3];
  report_wait.style.display = "none";

  let generated_report_div = document.getElementById("generated-report-stud-cum");
  generated_report_div.style.display = "block";

  let stud_cum_class_display = document.getElementById("stud-cum-report-class-display");
  stud_cum_class_display.innerHTML = data.class_name;

  let stud_cum_link = document.getElementById("stud-cum-report-download-link");
  stud_cum_link.href = data.file_path;
}


let generateStudCumRep = function (event) {
  console.log("generateStudCumRep");
  let class_id = document.getElementById("select-class-report").value;

  //   make report_wait appear
  let report_wait = document.getElementsByClassName("report-wait")[3];
  report_wait.style.display = "block";
  console.log(report_wait);

  // axios request
  axios({
    method: "get",
    url: "/reports/api/student-cumulative/?class_id=" + class_id,
  })
    .then((res) => generateStudCumHandler(res.data, class_id))
    .catch((err) => console.log(err));
};


let allClassStudCumRep = function (event) {
  console.log("allClassStudCumRep");
  document.getElementById("select-class-report").value = "all";
  generateStudCumRep(event)
}