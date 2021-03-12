email.onblur = function() {
  if (!email.value.includes('@') || !email.value.includes('.')) { // не email
    email.classList.add('invalid');
    error.innerHTML = 'Пожалуйста, введите правильный email.'
  }
};

email.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error.innerHTML = "";
  }
};
password.onblur = function() {
  if (password.value.length < 6)  { // не email
    password.classList.add('invalid');
    error_password.innerHTML = 'Пароль не должен быть короче 6 символов и должен содержать буквы и цифры.'
  } else if (password.value.search(/^([^0-9]*)$/) != -1 || password.value.search(/^([^a-z]*)$/) != -1) {
      password.classList.add('invalid');
      error_password.innerHTML = 'Пароль должен содержать буквы и цифры.'
    };
};

password.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error_password.innerHTML = "";
  }
};
phone.onblur = function() {
  if (phone.value.length < 9 || phone.value.search(/^([^a-z]*)$/) == -1 || phone.value.length > 12) { // не email
    phone.classList.add('invalid');
    error_phone.innerHTML = 'Пожалуйста, введите коректный номер.'
  }
};

phone.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error_phone.innerHTML = "";
  }
};

password2.onblur = function() {
  if (password2.value != password.value) { // не email
    password2.classList.add('invalid');
    error_password2.innerHTML = 'Пароли должны совпадать'
  }
};

password2.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error_password2.innerHTML = "";
  }
};