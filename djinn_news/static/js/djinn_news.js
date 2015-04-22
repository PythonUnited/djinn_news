/* JS for Djinn news */

$('iframe').each( function() {
    var url = $(this).attr("src")
    $(this).attr({
        "src" : url.replace('?rel=0', '')+"?wmode=transparent",
        "wmode" : "Opaque"
    })
});
