Pokemanki = {}

Pokemanki.addPokemanki = function(){
    let padDiv = document.createElement("div");
    // Set height manually because the scss rules somehow can't be loaded
    padDiv.setAttribute("style", "height: 5em;");
    let divEl = document.createElement("div");
    divEl.setAttribute("id", "pokemanki");
    divEl.setAttribute("style",
                       "margin: auto; text-align: center; width: fit-content");
    divEl.className = "pokemanki";
    let mainEl = document.getElementsByTagName("div")[0];
    mainEl.parentElement.insertBefore(padDiv, mainEl);
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
