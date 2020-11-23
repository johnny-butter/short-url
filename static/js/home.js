$(document).ready(function() {
    $("#shortlize").click(function() {
        $.ajax({
            url: "/v1/url",
            type: "POST",
            data: {"origin_url": $("#originUrl").val()},
            success: function(resp) {
                $("#shortUrl").attr("title", $("#originUrl").val());
                $("#shortUrl").attr("href", "/" + resp.short_url);
                $("#shortUrl").text(window.location.origin + "/" + resp.short_url);
            },
            error: function(err) {
                console.log(err.responseJSON);
                alert(err.responseJSON.message);
            }
        });
    });
});
