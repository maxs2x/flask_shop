function ChangeBgColor(id) {
  let idEl = 'btn' + id;
  let idTxt = 'text' + id;
  let elem = document.getElementById(idEl);
  let delActive = document.getElementsByClassName('active')[0];
  let hoverText = document.getElementById(idTxt);
  let delVisibaleText = document.getElementsByClassName('displayyes')[0];
  delVisibaleText.classList.add('display');
  delVisibaleText.classList.remove('displayyes');
  hoverText.classList.remove('display');
  hoverText.classList.add('displayyes');
  delActive.classList.remove('active');
  elem.classList.add('active');
}