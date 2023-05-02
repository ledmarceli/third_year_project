//Remove all content from the right column
function clearContent(){
    document.getElementById("1").innerHTML = "";
}

//Add content to the right column
function addContent(content){
    document.getElementById("1").innerHTML=content;
}

//Open lichess in a new window
function lichess(){
    url = "https://lichess.org/analysis"
    window.open(url, '_blank').focus();
    addContent("Lichess.org should load in a new window if you have internet connection.");
}

//Preview user manual
function manual(){
    clearContent();
    const element = document.getElementById("1");
    const pdf = document.createElement("Object");
    pdf.setAttribute("data","client/user_manual.pdf");
    pdf.setAttribute("type","application/pdf");
    element.appendChild(pdf);
}