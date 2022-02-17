console.log("backup.js");

let getBackup = function (event) {
  console.log("getBackup");
  let backup_wait = document.getElementById("backup-wait");
  backup_wait.style.display = "block";

  axios({
    method: "get",
    url: "/reports/backup/?action=now",
  })
    .then((res) => {
      console.log(res);
      backup_wait.style.display = "none";
      let latest_backup = document.getElementById("latest-backup");
      latest_backup.style.display = "block";
      let backup_link = document.getElementById("latest-backup-link");
      backup_link.href = res.data.backup_url;
    })
    .catch((err) => console.log(err));
};
