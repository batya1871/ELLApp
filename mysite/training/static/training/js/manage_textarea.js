window.onload = function() {
    var textareas = document.querySelectorAll('textarea'); // Получаем все элементы textarea на странице

    // Проходимся по каждому элементу textarea
    textareas.forEach(function(textarea) {
        if (!textarea.hasAttribute('readonly')) { // Проверяем, не имеет ли textarea атрибута "readonly"
            textarea.value = ''; // Если нет, стираем текст внутри
        }
        else{
            textarea.value = textarea.value.trimStart();
        }
    });
};
