$(function() {
    $('#fileupload').fileupload({
        width: 300,
        url: 'upload',
        dataType: 'json',
        replaceFileInput:false,
        add: function(e, data) {
            data.submit()
        },
        success: function(response, status) {
            var filePath = 'static/uploads/' + response.filename
            $('#imgUpload').attr('src', filePath)
            $('#container-pred').removeClass("hidden")
            $('#filePath').text(filePath)
            $('#pred').text(' ')
            $('.container-pred #validate').text(' ')
        },
        error: function(error) {
            console.log(error)
        }
    })
})
$(function() {
    $('#predict').click(function(e) {
        e.preventDefault()
        $('#predict').text('Predicting...')
        data = {f_name:$('#filePath')[0].textContent}
        $.ajax({
            type: "POST",
            url: "/predict",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(response, status) {
                pred = response.pred
                $('#pred').text(pred)
                $('#predict').text('Predict')
                $('.container-pred #validate')[0].innerHTML = "Is this correct? <span class = 'btn-validate' id = 'yes' onclick=user_validate(true)>Yes</span> | <span class = 'btn-validate' id = 'no' onclick=user_validate(false)>No</span>"
            },
            error: function(result) {
                console.log(error)
            }
        })
    })
})
$(function() {
    $('#slide-down').click(function() {
        $('#txt-content').slideToggle()
    })
})

function user_validate(is_correct) { 
    if (is_correct) { 
        $('.container-pred #validate')[0].innerHTML = "Thank you for your feedback!"
    } else { 
        $('.container-pred #validate')[0].innerHTML = "Oh no! Logging this!"
        data = {f_name:$('#filePath')[0].textContent}
        $.ajax({
            type: "POST",
            url: "/upload_to_dropbox",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(response, status) {
                console.log("uploaded to Dropbox!")
            },
            error: function(result) {
                console.log(error)
            }
        })
    }
}

