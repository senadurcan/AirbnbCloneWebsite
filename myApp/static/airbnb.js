
const rangeInput = document.querySelectorAll(".range-input input"),
priceInput = document.querySelectorAll(".price-input input"),
progress =  document.querySelector(".main-slider .progress");

let priceGap = 500 ;

priceInput.forEach(input =>{
    input.addEventListener("input",e=>{
        // iki input değeri alma ve bunları iki sayı ayrıştırma
        let minVal = parseInt(priceInput[0].value),
        maxVal = parseInt(priceInput[1].value);

        if((maxVal - minVal >= priceGap) && maxVal <= 10000){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minVal ;
                progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            }else{
                rangeInput[1].value = maxVal ;
                progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
            }
            
        }
                
    })
});


rangeInput.forEach(input =>{
    input.addEventListener("input",e=>{
        // iki aralık değeri alma ve bunları iki sayı ayrıştırma
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        if(maxVal - minVal < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap ;
            }else{
                rangeInput[1].value = minVal + priceGap ;
            }
            
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
            progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }
        
        
    })
});


fetch("https://countriesnow.space/api/v0.1/countries/population/cities")
.then(response => response.json())
.then(data =>{
    let optionCountry = document.getElementById("country");
    
    data.data.forEach(element => {
        let myOption = document.createElement("option")
        myOption.innerHTML=`${element.city} , ${element.country}`
        
        optionCountry.appendChild(myOption)
    });
})


// ----------------------POST-PAYLAŞMA-FORMU-JS-------------------

var form = document.getElementById('step-form');
var nextBtns = document.querySelectorAll('[id^=next-btn]');
var prevBtns = document.querySelectorAll('[id^=prev-btn]');
var formSteps = form.getElementsByClassName('form-step');
var first = document.getElementById("first");
var second = document.getElementById("second");
var btn = document.getElementById('btn');
var fileInput = document.getElementById("file-input");
var fileList = document.getElementById("files-list");
var numOfFiles = document.getElementById("num-of-files");

var fileInput2 = document.getElementById("file-input2");
var fileList2 = document.getElementById("files-list2");
var numOfFiles2 = document.getElementById("num-of-files2");


var step = 0;

function myFunction() {
  if (first.style.display == "block") {
    first.style.display = "none";
    second.style.display = "block";
    btn.style.display= "none";
  } else {
    first.style.display = "none";
    second.style.display = "block";
    btn.style.display= "none";

  }
}

for (var i = 1; i < formSteps.length; i++) {
  formSteps[i].style.display = 'none';
}

for (var i = 0; i < nextBtns.length; i++) {
  nextBtns[i].addEventListener('click', function() {
    formSteps[step].style.display = 'none';
    step++;
    formSteps[step].style.display = 'block';
  });
}

for (var i = 0; i < prevBtns.length; i++) {
  prevBtns[i].addEventListener('click', function() {
    formSteps[step].style.display = 'none';
    step--;
    formSteps[step].style.display = 'block';
  });
}


// ----------------------HOST-RANGE-SLİDER-------------------
var output = document.getElementById("demo");

var slider = document.getElementById("myRange").oninput = function (){

  var value = (this.value-this.min)/(this.max-this.min)*100

  this.style.background = 'linear-gradient (to right, #838383 0%, #838383' + value + '%, #838383' + value + '%, #838383 100%)'

  output.innerHTML = this.value;


}

