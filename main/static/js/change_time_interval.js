$(document).ready(function () {
    // Живой поиск
    var date = $('#datetimepicker7').val();
    var time = $('#time_select').val();
    var post_query = function () {
        console.log("gg");

        $.ajax({
            url: $("#url_this_page").attr("data-url"), // url текущей странички
            data: {
                gg: $("#search").val(), // значения из инпут поля
                date_start: $("#date_start").val(),
                time_choice: $('#time_select option:selected').text(),
            },
            data_type: "html",
            type: "GET",
            // если успешно, то
            success: function (data) {
                console.log(data)
                $('#aboba').html(data);
            },
            error: function (xhr, errmsg, err) {
                alert("Could not send URL to Django. Error: " + xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    }
    $("#search").keyup(post_query);
    var time_func = function(){
        var input_time = $("#time_select option:selected");
        var old_time = $("#time_select").attr("time-old-value");
        var current_time = input_time.text();
        console.log("CUR ", current_time);
        console.log("OLD", old_time);

        var input = $("#date_start");
        var old = input.attr("data-old-value");
        var current = input.val();
        console.log("OLD2", old);
        if ((old !== current) || (old_time !== current_time)) {
            if ((typeof old != 'undefined') || (typeof old_time != 'undefined') ) {
                console.log("ПОСТ ПРОИЗАШЕЛ ИНФА 100")
                post_query();
            }
            input.attr("data-old-value", current);
            $("#time_select").attr("time-old-value", current_time);
        }

    };
    setInterval(time_func, 600);
});