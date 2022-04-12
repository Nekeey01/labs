$(document).ready(function () {
    // Алерт при нажатии на кнопку брони
    $("button").click(function (e) {
        e.preventDefault();
        var me = this; // установка контекста
        $.ajax({
            url: $("#url_this_page").attr("data-url"),
            data: {
                click: true,
                csrfmiddlewaretoken: $("#csrf_token").attr("data")
            },
            type: "POST",
            // если успешно, то
            success: function (data) {
                if (data.status == 1) {
                    console.log("боба");

                    window.location.assign(
                        $(me).attr("data-url") // переход на ссылку, которая установлена в кнопке "забронировать"
                    );
                } else if (data.status == 0) {
                    // Красивый alert
                    Swal.fire({
                        icon: 'warning',
                        title: 'Авторизируйтесь или зарегестрируйтесь для продолжения!',
                        showDenyButton: true,
                        showCancelButton: true,
                        confirmButtonText: 'Авторизация',
                        denyButtonText: `Регистрация`,
                        cancelButtonText: `Закрыть`,
                    }).then((result) => {
                        if (result.isConfirmed) {
                            $('#login_modal').click(); // открытие окна логина
                        } else if (result.isDenied) {
                            $('#register_modal').click(); //  открытие окна регистрации
                        }
                    })
                }
                console.log("выполнилось");
            },
            error: function (xhr, errmsg, err) {
                alert("Случилась АБОБА. Во всем виноват путин. Error: " + xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    });
});