$(document).ready(function () {
    $('form').each(function (i, v) {
        var $form = $(v),
            errors = $form.data('errors');
        $form.find('.form-control').each(function (i, v) {
            var $input = $(v);

            if (errors[$input.attr('name')] !== undefined) {
                var errors_html = '';
                $.each(errors[$input.attr('name')], function (i, v) {
                    errors_html += '<span style="color:red">' + v + '</span>';
                });
                $input.closest('div').append(errors_html);
                $input.closest('.form-group').addClass('has-error');
            }
        });
    });
});