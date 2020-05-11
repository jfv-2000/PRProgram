var setNumber = 1
const maxSet = 20
$(document).ready(function () {
    $("#add").click(function (e) {
        if (setNumber < maxSet) {
            setNumber++
            console.log(setNumber)
            var appendthis = ('<div id="formRow">&nbsp<input type="number" name="reps['+setNumber+']" class="PR" placeholder="#reps" required>' +
                '&nbsp<input type="number" required name="percent['+setNumber+']" class="PR" placeholder="%PR">'
                + '&nbsp<button type="button" value="delete" class="btn btn-danger delete" id="delete">Remove</button></div>')
            $('#formRow').append(appendthis)
            document.getElementById('numSet').value = setNumber
        } else {
            var errorMax = document.getElementById("maxSet")
            errorMax.innerHTML = "20 Sets is the Max ! Sorry !"
            console.log("MAX")
        }
    })


    $('body').on('click', '#delete', function (e) {
        $(this).parent('div').remove()
        setNumber--
        document.getElementById('numSet').value = setNumber
        console.log(setNumber)
    })
})
document.getElementById('numSet').value = setNumber
