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
            $('#imgUpload').attr('src',filePath)
            $('#container-pred').removeClass("hidden")
            $('#filePath').text(filePath)
            $('#pred').text(' ')
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