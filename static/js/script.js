// Code gotten from https://codepen.io/NaokiIshimura/pen/aEvQPY
$(document).ready(function($) {
    $(".table-row").click(function() {
        window.document.location = $(this).data("href");
    });
});