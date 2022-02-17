console.log('concession.js');

let addConcession = function (event) {
    console.log('addConcession');
    let concession_sec = document.getElementById('add-concession');
    concession_sec.classList.toggle('hidden');
}

let addMisc = function (event) {
    console.log('addMisc');
    let misc_sec = document.getElementById('add-misc');
    misc_sec.classList.toggle('hidden');
}