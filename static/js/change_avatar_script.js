document.addEventListener("DOMContentLoaded", function () {
    const avatarUpload = document.getElementById("avatarUpload");

    avatarUpload.addEventListener("change", function () {
        const formData = new FormData();
        formData.append("avatar", avatarUpload.files[0]);

        // Отправьте файл на сервер с использованием AJAX или Fetch API
        fetch("/user/profile/change-avatar/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrf_token // Если вы используете CSRF-защиту
            }
        })
            .then(response => response.json())
            .then(data => {
                location.reload();
                // Обработка ответа от сервера (например, обновление аватара на странице)
            })
            .catch(error => {
                console.error("Произошла ошибка при отправке файла на сервер:", error);
            });
    });
});