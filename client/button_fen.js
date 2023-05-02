//Remove all content from the right column
function clearContent(){
    document.getElementById("1").innerHTML = "";
}

//Add content to the right column
function addContent(content){
    document.getElementById("1").innerHTML=content;
}

//Handle Fen functionality:
function fen(content){
    addContent(content);
    //Create the form in the right column
    const element = document.getElementById("1");
    const nextL = document.createElement("br");
    element.appendChild(nextL);
    //Form
    const form = document.createElement("form");
    const label = document.createElement("label");
    const textToLabel = document.createTextNode("Input the FEN position: ");
    const input = document.createElement("input");
    input.setAttribute("type","text");
    input.setAttribute("id","position");
    label.setAttribute("for","position");
    label.appendChild(textToLabel);
    const label2 = document.createElement("label");
    const textToLabel2 = document.createTextNode("Input the move in form e2e4: ");
    const input2 = document.createElement("input");
    input2.setAttribute("type","text");
    input2.setAttribute("id","move");
    label2.setAttribute("for","move");
    label2.appendChild(textToLabel2);
    //Submit button
    const button = document.createElement("Button");
    const textToButton = document.createTextNode("Submit");
    button.setAttribute("onClick","submitPosition()");
    button.appendChild(textToButton);
    //Append elements to form
    form.appendChild(label);
    form.appendChild(nextL.cloneNode());
    form.appendChild(input);
    form.appendChild(nextL.cloneNode());
    form.appendChild(label2);
    form.appendChild(nextL.cloneNode());
    form.appendChild(input2);
    form.appendChild(nextL.cloneNode());
    form.appendChild(button);   
    element.appendChild(form);
    document.getElementById("move").style.width = "6%";
}

//Submits the move and position for processing
function submitPosition(){
    const position = document.getElementById("position").value;
    const move = document.getElementById("move").value;
    data = {position : position, move : move};
    clearContent();
    addContent("Processing...It may take a minute.");
    fetch('http://localhost:8080/api', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    //Once the response is received, output the response.
    .then(response => response.json())
    .then(data => {
        var output = data["output"];
        output = output.replace("\r","");
        output = output.replace("\n","");
        fen(output);
    })
    .catch(error => console.error(error));
}




