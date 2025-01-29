$('#mail_form').on('submit', function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.ajax(
        {
            'url': $(this).attr('action'),
            'method': $(this).attr('method'),
            'data': formData,
            'type': 'POST',
            'dataType': 'json',
            'success': function (data) {
                if (data.form_is_valid) {
                    $('#mail_form').hide();
                    $('#mail_success').show();
                }
                else {
                    $('#mail_form').show();
                    $('#mail_success').hide();
                }

            },
            'error': function (xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        }
    );

})