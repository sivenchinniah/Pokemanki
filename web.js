Pokemanki = {}

Pokemanki.addPokemanki = function(){
    let padDiv = document.createElement("div")
    padDiv.setAttribute("class", "range-box-pad")
    let divEl = document.createElement("div");
    divEl.setAttribute("id", "pokemanki")
    divEl.className = "pokemanki";
    let mainEl = document.getElementById('main');
    mainEl.parentElement.insertBefore(padDiv, mainEl)
    mainEl.parentElement.insertBefore(divEl, mainEl);
}
Pokemanki.setPokemanki = function(html){
    document.getElementById('pokemanki').innerHTML = html;
}

Pokemanki.initialLoad = function(){
    if(document.getElementsByTagName("input").length < 3){
        return
    }
    window.clearInterval(Pokemanki.initLoadInterval);
    Pokemanki.addPokemanki();
    Pokemanki.deckRadio = document.getElementsByTagName("input")[0];
    Pokemanki.colRadio = document.getElementsByTagName("input")[1];
    Pokemanki.textInput = document.getElementsByTagName("input")[2];
    Pokemanki.deckRadio.addEventListener("input", function(e){
        if(e.target.value){
            pycmd("Pokemanki#currentDeck");
        }
    })
    Pokemanki.colRadio.addEventListener("input", function(e){
        if(e.target.value){
            pycmd("Pokemanki#wholeCollection");
        }
    })
    Pokemanki.textInput.addEventListener("keyup", function(e){
        if(e.key == "Enter"){
            searchStr = e.target.value;
            pycmd("Pokemanki#search#" + searchStr);
        }
    })
    if(Pokemanki.deckRadio.value){
        html = pycmd("Pokemanki#currentDeck");
    }else{
        pycmd("Pokemanki#wholeCollection");
    }
}
Pokemanki.initLoadInterval = window.setInterval(Pokemanki.initialLoad, 50);