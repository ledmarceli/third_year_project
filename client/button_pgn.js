const e = require("cors");

//Clears all contents in right column
function clearContent(){
    document.getElementById("1").innerHTML = "";
}

//Adds content to the right column
function addContent(content){
    document.getElementById("1").innerHTML=content;
}

//Handles the PGN
function pgn(){
    //Creating the form
    addContent("Upload the PGN file for processing.");
    const element = document.getElementById("1");
    const nextL = document.createElement("br");
    element.appendChild(nextL);
    const form = document.createElement("form");
    form.setAttribute("action","upload");
    form.setAttribute("method","POST");
    form.setAttribute("enctype","multipart/form-data");
    const input = document.createElement("input");
    input.setAttribute("type","file");
    input.setAttribute("accept",".pgn, .txt");
    input.setAttribute("id","pgn");
    input.setAttribute("name","fileInput");
    const label = document.createElement("label");
    const textToLabel = document.createTextNode("Input the name of the Player to investigate: ");
    const input2 = document.createElement("input");
    input2.setAttribute("type","text");
    input2.setAttribute("id","player");
    label.setAttribute("for","player");
    label.appendChild(textToLabel);
    const button = document.createElement("Button");
    const textToButton = document.createTextNode("Submit");
    button.setAttribute("type","submit()")
    button.appendChild(textToButton);
    form.appendChild(input);
    form.appendChild(nextL.cloneNode());
    form.appendChild(label);
    form.appendChild(nextL.cloneNode());
    form.appendChild(input2);
    form.appendChild(nextL.cloneNode());
    form.appendChild(button);
    element.appendChild(form);

    const form1 = document.querySelector('form');
    const fileInput = document.querySelector('input[type="file"]');
    //Submit pgn and player name for processing
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // prevent the form from submitting normally
        const textInput = document.getElementById("player").value;
        addContent("Processing... It might take up to a few minutes.");

      
        const formData = new FormData();
        formData.append('file', fileInput.files[0], 'game.pgn');
        formData.append('text', textInput);
        fetch('http://localhost:3000/upload', {
          method: 'POST',
          body: formData
        })
        //Once the reponse is received
        .then(response => response.json())
        .then(data => {
            var output = data["output"];
            output = output.replace("\r","");
            output = output.replace("\n","");
            //For error messages
            if (!output.startsWith("[")){
                addContent(output); 
            } 
            else{
                const array = JSON.parse(output)
                console.log(array);
                //Check if any moves were run through the model
                if(array.length<2){
                    addContent("Not enough moves to run the prediction")
                }
                else{
                    //Calculate the general overview data
                    const element = document.getElementById("1");
                    var suspicious = 0;
                    var undecided = 0;
                    var gameCount = 0;
                    for (let i=0;i<array.length;i++){
                        if (array[i]>100){
                            gameCount = gameCount+1;
                        }
                        else if (array[i]>75){
                            suspicious = suspicious+1;
                        }
                        else if (array[i]>30){
                            undecided = undecided+1;
                        }
                    }
                    var report = "The number of moves considered was "+array.length+".<br>"+suspicious+" had high engine envolvement prediction.<br>"+undecided+" had a moderate engine envolvement prediction.<br>";     
                    addContent(report);
                    var moveCount = 16;
                    //Generate output
                    for(let i=0;i<array.length;i++){
                        if (array[i]>100){
                            var game = document.createElement("ul");
                            game.textContent = "Game " + ((array[i]-1)/100) +":";
                            element.appendChild(game)
                            moveCount = 16;
                        }
                        else{
                            var move = document.createElement("li")
                            move.textContent = "Move "+moveCount + ": " + array[i]+"%";
                            if (array[i]>=75){
                                move.style.color = 'Red';
                            }
                            else if (array[i]>=30){
                                move.style.color = 'Gold';
                            }
                            else{
                                move.style.color = "Green";
                            }
                            game.appendChild(move)
                            moveCount = moveCount+1;
                        } 
                    }
                }
            }
        })
        .catch(error => console.error(error));
      });
    }