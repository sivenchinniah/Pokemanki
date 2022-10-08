/* Pokémanki
 * Copyright (C) 2022 Exkywor and zjosua
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

Pokemanki = {}

Pokemanki.addPokemanki = function(){
    let divEl = document.createElement("div");
    divEl.setAttribute("id", "pokemanki")
    divEl.className = "pokemanki";
    let rangeBoxPad = document.querySelector('.range-box-pad');
    rangeBoxPad.after(divEl);

    link = document.createElement('link');
    link.href = "/pokemanki_css/view_stats.css";
    link.rel = 'stylesheet';
    document.head.appendChild(link);
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
