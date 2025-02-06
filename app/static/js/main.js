document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript загружен!");

    // Добавляем анимацию при загрузке страницы
    let elements = document.querySelectorAll(".fade-in");
    elements.forEach(el => el.classList.add("visible"));

    // Проверяем, был ли выход из аккаунта
    if (sessionStorage.getItem("loggedOut") === "true") {
        console.log("🔄 Обнаружен выход из аккаунта! Перезагружаем страницу.");
        sessionStorage.removeItem("loggedOut"); // Сбрасываем флаг
        location.reload();  // Принудительно обновляем страницу
    }
});

// При выходе из аккаунта
function logout() {
    sessionStorage.setItem("loggedOut", "true");
    // Дополнительный код для выхода из аккаунта
}