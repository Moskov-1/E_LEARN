function getCSRFToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}
$(document).on('submit', '#mail_form', function (e) {
    e.preventDefault();
    console.log("Form submitted!");
    const formData = $(this).serialize();

    $('#mail_form').on('submit', function (e) {
        e.preventDefault();
        
        $('#mail_form').focus(); // Force focus on the form
        $('#mail-submit-button').prop('disabled', true); // Disable button before sending request
        
        const formData = $(this).serialize();
        
        $.ajax(
            {
                'url': $(this).attr('action'),
                'method': $(this).attr('method'),
                'data': formData,
                'type': 'POST',
                'dataType': 'json',
                'headers': {
                    "X-CSRFToken": getCSRFToken()  // Include CSRF token
                },
                'success': function (data) {
                if (data.success) {
                    $('#worked_message').text('Email sent successfully!').css('color', 'green').removeClass('d-inline-block').show();
                    $('#mail_form')[0].reset();
                } else {
                    $('#worked_message').text('Failed to send email. Please try again.').removeClass('d-inline-block').css('color', 'red').show();
                }
                },
                'error': function (xhr, errmsg, err) {
                    console.log(xhr.status + ': ' + xhr.responseText);
                    $('#worked_message').text('An error occurred. Please try again later.').css('color', 'red').show();
                },
                complete: function () {
                    $('#mail-submit-button').prop('disabled', false); // Enable button after request completes
                },
        
            }
        );

       
           
           
       
    
    });

   

})