const all_row = document.querySelectorAll('.row-curator');
all_row.forEach(el=>{
    let sum_for_all_quart = 0;
    el.querySelectorAll('.quart').forEach((item)=>{
        sum_for_all_quart += Number(item.textContent);
    })
    el.children[5].textContent = sum_for_all_quart;
})


let result_money = [];
for (let i = 1; i<= 5; i+=1){
    let sum_for_quart = 0;
    all_row.forEach((row) =>{
      sum_for_quart +=  Number(row.querySelectorAll('td')[i].textContent)
    })
    result_money.push(sum_for_quart);
    
}

const all_td_result = document.querySelectorAll('.result-money');
all_td_result.forEach((el,index) => {
    el.textContent = result_money[index]
})


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }


const json = JSON.stringify(result_money);
const csrftoken = getCookie('csrftoken');

const cost_title = document.querySelector('.cost-title').textContent;

fetch('/plane/to_server/', {
        'method': 'POST',
        'credentials': 'include',
        'headers': new Headers({
          'X-CSRFToken': csrftoken,
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        }),
        'body': JSON.stringify({
            cost_title: cost_title,
            result_money: result_money,
            data_from_django: data_from_django
        }),
        'mode':'cors',
        'cache':'default',
        'credentials':'include'      
    })
