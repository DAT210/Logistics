$(document).ready(function () {
    console.log("HELLO")

    $('newLocForm').on('sumbit', function(event) {
        event.preventDefault();
        var data = {locationName : $("#newLocationName").val()};
        var dataJson = JSON.stringify(data)

        $.ajax({
            dataJson,
            type : 'POST',
            url : '/v1/locations/'
        })
        .done(function(data) {
            if (data.code) {

            } else {
                $('#successAlert').text("Created new location!").show()
            }
        })
    });
});
