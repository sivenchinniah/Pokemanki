Pokemanki = {}

Pokemanki.addPokemanki = function(){
    let divEl = document.createElement("div");
    divEl.setAttribute("id", "pokemanki")
    divEl.className = "pokemanki";
    let rangeBoxPad = document.querySelector('.range-box-pad');
    rangeBoxPad.after(divEl);

    link1 = document.createElement('link');
    link1.href = "/pokemanki_css/view_stats.css";
    link1.rel = 'stylesheet';

    link2 = document.createElement('link');
    link2.href = "/pokemanki_css/main.css";
    link2.rel = 'stylesheet';

    document.head.appendChild(link1);
    document.head.appendChild(link12;
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