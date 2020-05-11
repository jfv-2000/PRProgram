console.log("BITCH")
console.log("why")

var i = 0;
$('.programclass').each(function () {
    i++;
    var newID = 'program_name' + i;
    $(this).attr('id', newID);
    $(this).val(i);
});

var x
var programName
var showName = document.getElementById("nameofprogram")
var clicked = false
var arrName = new Array(i)

for (x = 0; x < i; x++) {
    arrName[x] = document.getElementById("program_name" + (x + 1))
    console.log(arrName[x].textContent)
}




