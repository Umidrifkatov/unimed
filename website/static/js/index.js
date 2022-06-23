








let baseurl = 'https://unimedtrade.uz/'

if (window.Telegram.WebApp){
    var tg = window.Telegram.WebApp;
    var text_color = tg.themeParams.text_color;
    var bg_color = tg.themeParams.bg_color;  
}



async function getData(){
    let url = baseurl + 'api/products'
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}




var search = document.getElementById('input-search')
var els = document.getElementsByClassName('forsearch')
search.addEventListener("keyup", function() {
    Array.prototype.forEach.call(els, function(el) {
      if (el.textContent.trim().indexOf(search.value) > -1)
        el.style.display = 'block';
      else el.style.display = 'none';
    });
  
  });



var select1 = document.getElementById('selectcat')
select1.addEventListener('change', function(){
    Array.prototype.forEach.call(els, function(el) {
    if (select1.value == 'all')
        el.style.display = 'block';
    else
        if (el.textContent.trim().indexOf(select1.value) > -1)
          el.style.display = 'block';
        else el.style.display = 'none';
      });
    
    });
  


var select2 = document.getElementById('selectman')
select2.addEventListener('change', function(){
    Array.prototype.forEach.call(els, function(el) {
    if (select2.value == 'all')
        el.style.display = 'block';
    else
        if (el.textContent.trim().indexOf(select2.value) > -1)
          el.style.display = 'block';
        else el.style.display = 'none';
      });
    
    });






async function createlist(){
    let list = await getData()
    let wrapper = document.getElementById('list-wrapper')
    let categorys1 = new Set()
    let manufac1 = new Set()
    for (var z in list){

        categorys1.add(list[z].category_name)
        manufac1.add(list[z].manufacturer_name)
    }
    let categorys = Array.from(categorys1)
    let manufacturer = Array.from(manufac1)
    
    
    for(var g in categorys){
        let option = new Option(categorys[g], categorys[g])
        console.log(categorys[g])
        let pep = document.getElementById('selectcat')
        pep.add(option, undefined)
        
    }

    for (var k in manufacturer){
        let option = new Option(manufacturer[k], manufacturer[k])
        console.log(manufacturer[k])
        let pep = document.getElementById('selectman')
        pep.add(option, undefined)

    }

    console.log(categorys)




    for (var i in list){
            
        var item = `
        <div class="forsearch" onclick="changepage(${i})">
        <div class=" d-flex justify-content-between align-items-center" >
        <div>
            <h5 class=" mb-0 mt-1 p-0">  ${list[i].name}</h5>
            <small class="m-0 p-0">  ${list[i].category_name} ${list[i].manufacturer_name} </small> 
        </div>
        <h4>
            <span> <i class="fa-solid fa-angle-right"></i></span>
        </h4>
        </div>
        <p hidden> ${list[i].name.toLowerCase()} ${list[i].category_name.toLowerCase()} ${list[i].manufacturer_name.toLowerCase()}</p>
        <hr class="m-0 p-0" >
        </div>
        `
        wrapper.innerHTML += item
    }
    console.log(list)
}

async function changepage(elementid){
    let using = document.getElementById('secondcontent')
  
    let url = baseurl + `api/product/${elementid + 1}`;
    fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let list = data;
      console.log(list)
      if(list.is_used) {
          list.is_used = 'Использованный'
      }else{
        list.is_used = 'Новый'
      }
      datainsert = `
        <h2 class="mt-2 mb-2 container d-flex justify-content-between align-items-center backicons" onclick="back()">
        
            <i class="fa-solid fa-angle-left"></i>
            <i class="fa-solid fa-xmark"></i>

        </h2>
        <div class="text-center image img-fluid mb-2">
        
            <img src="${baseurl+ 'media/' + list.img_url[0]}" class="rounded" alt="">
        </div>
        <h3> ${list.name} </h3>
        <hr class="m-0 p-0">
        <div class="d-flex justify-content-between align-items-center mb-4" >
            <small>${list.manufacturer_name} ${list.category_name}</small>
            <small>${list.is_used}</small>
        </div>
        <h6 class="mb-0">Описание</h6>
        <hr class="mt-0">
        <p>${list.short_description}</p>
        <hr>
        <p>${list.long_description}</p>
        <p>${list.technical_details}</p>

            
    `  
    using.innerHTML = ''
    using.innerHTML += datainsert


    })

    
           
    





    document.getElementById('maincontent').style.display = 'none'
}


function back(){
    document.getElementById('maincontent').style.display = 'block'
    let using = document.getElementById('secondcontent')
    using.innerHTML = ''
}


createlist()




  
