$(function() {
    function updateErrorList(errors) {
        const errorList = $("#error_list");
        errorList.empty();
        if (errors.length === 0) {
            errorList.append("<li>No errors detected yet.</li>");
        } else {
            errors.forEach(function(error) {
                const timestamp = new Date(error.timestamp * 1000).toLocaleString();
                errorList.append(`<li>${timestamp}: ${error.errors.join(", ")}</li>`);
            });
        }
    }

    function fetchErrors() {
        $.ajax({
            url: "/api/plugin/ai_error_detection",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({ command: "get_detections" }),
            contentType: "application/json",
            success: function(response) {
                updateErrorList(response.detections);
            }
        });
    }

    $("#refresh_errors").click(fetchErrors);
    fetchErrors();  // Initial fetch on page load
});
