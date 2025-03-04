document.addEventListener("DOMContentLoaded", function () {

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

function scrollToBottom() {
    let chatMessages = document.querySelector(".chat-messages");
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Обработка события htmx:oobAfterSwap
document.addEventListener("htmx:oobAfterSwap", function(event) {
    scrollToBottom();
});

// Обработка события DOMContentLoaded
document.addEventListener("DOMContentLoaded", function() {
    scrollToBottom();
});