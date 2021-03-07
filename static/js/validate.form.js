email.onblur = function() {
  if (!email.value.includes('@')) { // не email
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
  if (password.value() == password2.value()) { // не email
    password.classList.add('invalid');
    error.innerHTML = 'Пожалуйста, введите правильный email.'
  }
};

password.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error.innerHTML = "";
  }
};


phone.onblur = function() {
  if (!phone.value.includes('1' or '2' or '3')) { // не email
    phone.classList.add('invalid');
    error.innerHTML = 'Пожалуйста, введите правильный email.'
  }
};
phone.onfocus = function() {
  if (this.classList.contains('invalid')) {
    // удаляем индикатор ошибки, т.к. пользователь хочет ввести данные заново
    this.classList.remove('invalid');
    error.innerHTML = "";
  }
};