(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()

const button = document.getElementById('reset-btn');
const inputs = document.querySelectorAll('.email-input input');


if ( button != null){
  inputs.forEach(function(input) {
    // Добавляем класс 'form-control' к текущему элементу
    input.classList.add('form-control');
    input.required = true;
    input.placeholder = 'Эл. почта';
});
}

const button_new_pass = document.getElementById('new-pass-btn');
const inputs_new_pass = document.querySelectorAll('.form-new-pass .form-obj-set input');


if ( button_new_pass != null){
 inputs_new_pass[0].placeholder = 'Пароль';
  inputs_new_pass[1].placeholder = 'Повторите пароль';
  inputs_new_pass.forEach(function(input) {
    // Добавляем класс 'form-control' к текущему элементу
    input.classList.add('form-control');
    input.required = true;
});
}