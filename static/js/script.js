
$(document).ready(function($) {
    // Code gotten from https://codepen.io/NaokiIshimura/pen/aEvQPY
    // Shows error but code has not been altered from the source
    $(".table-row").click(function() {
        window.document.location = $(this).data("href");
    });
    $('#session-detail-list a').on('click', function (e) {
        e.preventDefault()
        $(this).tab('show')
    });
});