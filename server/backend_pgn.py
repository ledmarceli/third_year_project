import sys
from run_model import run_model, check_pgn
from process_pgn import process_pgn
from network import initialise_model

#Get inputs
FILE_NAME = sys.argv[1]
PLAYER = sys.argv[2]

#Check if the file is a valid PGN
if not check_pgn(FILE_NAME):
    print("Something is wrong with your PGN file.")
else:
    #Analyse
    pgn = open(FILE_NAME)
    leela_output = process_pgn(pgn, PLAYER)
    pgn.close()
    #Run the values through the model
    predictions = []
    model = initialise_model()
    for leela in leela_output:
        #If label for the game, ignore
        if isinstance(leela, int):
            prediction = leela
        #If all the moves have the same evaluation, set to undecided.
        elif leela == [0,0,0,0,0]:
            prediction = (50.0)
        else:
            prediction = run_model(model,leela)
        predictions.append(prediction)
    print(predictions)
