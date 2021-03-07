function SelectTab(id) {
    let idEl = 'btn' + id;
    let idTxt = 'text' + id;
    let elem = document.getElementById(idEl);
    let delActive = document.getElementsByClassName('hover-tab')[0];
    let hoverText = document.getElementById(idTxt);
    let delVisibaleText = document.getElementsByClassName('displayyes')[0];
    delVisibaleText.classList.add('display');
    delVisibaleText.classList.remove('displayyes');
    hoverText.classList.remove('display');
    hoverText.classList.add('displayyes');
    delActive.classList.remove('hover-tab');
    elem.classList.add('hover-tab');
}
function Calculate(symbol) {
    let count = Number(document.getElementsByClassName('input-group-text')[0].innerHTML);
    let maxCount = Number(document.getElementById('maxCount').innerHTML);
    let newCount = 0;
    if (symbol == '-') {
        if (count > 0) {
            newCount = count - 1;
        }
    } else {
        if (maxCount > count) {
            newCount = count + 1;
        }
        else {
            if (document.getElementsByClassName('alert')[0]) {
                newCount = count;
            } else {
                let interElem = document.getElementById('alert-before')
                let divEl = document.createElement('div');
                divEl.className = "alert";
                divEl.innerHTML = "<strong>Вы не можете купить больше, чем есть на складе</strong>";
                interElem.append(divEl);
                newCount = count;
            }
        }
    }
    document.getElementsByClassName('input-group-text')[0].innerHTML = newCount;
}

function addInCart(id) {
    let countProduct = Number(document.getElementById('count-product').innerHTML)
    let form = document.createElement('form');
    form.method = 'POST';
    form.innerHTML = `<input name="add_id" value="${id}"><input name="number_of_additions" value="${countProduct}">`;
    document.body.append(form);
    form.submit();
}

function alertInCart(id) {
    if (document.getElementsByClassName('alert')[0]) {
        let clear = document.getElementsByClassName('alert')[0];
        clear.remove();
    }
    let interElem = document.getElementById(id);
    let divEl = document.createElement('div');
    divEl.className = "alert";
    divEl.innerHTML = "<strong>Вы не можете купить больше, чем есть на складе</strong>";
    interElem.append(divEl);
}