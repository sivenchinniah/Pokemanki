Pokemanki = {}

Pokemanki.addPokemanki = function(){
<<<<<<< HEAD:web.js
    let padDiv = document.createElement("div");
    // Set height manually because the scss rules somehow can't be loaded
    padDiv.setAttribute("style", "height: 5em;");
=======
>>>>>>> main:src/pokemanki/web.js
    let divEl = document.createElement("div");
    divEl.setAttribute("id", "pokemanki");
    divEl.setAttribute("style",
                       "margin: auto; text-align: center; width: fit-content");
    divEl.className = "pokemanki";
<<<<<<< HEAD:web.js
    let mainEl = document.getElementsByTagName("div")[0];
    mainEl.parentElement.insertBefore(padDiv, mainEl);
    mainEl.parentElement.insertBefore(divEl, mainEl);
=======
    let rangeBoxPad = document.querySelector('.range-box-pad');
    rangeBoxPad.after(divEl);

    link = document.createElement('link');
    link.href = "/pokemanki_css/view_stats.css";
    link.rel = 'stylesheet';
    document.head.appendChild(link);
>>>>>>> main:src/pokemanki/web.js
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
