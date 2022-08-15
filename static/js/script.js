// Code gotten from https://codepen.io/NaokiIshimura/pen/aEvQPY
// Shows error but code has not been altered from the source
$(document).ready(function($) {
    $(".table-row").click(function() {
        window.document.location = $(this).data("href");
    });
});