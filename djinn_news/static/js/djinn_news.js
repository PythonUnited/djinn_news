/* JS for Djinn news */
$(document).ready(function () {
    $('iframe').each(function () {
        var url = $(this).attr("src")
        $(this).attr({
            "src": url.replace('?rel=0', '') + "?wmode=transparent",
            "wmode": "Opaque"
        })
    });
});