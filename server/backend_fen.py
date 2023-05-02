import sys
import pandas as pd
import torch
from analyse import analyse, open_engine, close_engine
from process_pgn import check_move, extract_data
from run_model import run_model, is_valid
from network import initialise_model

NODES = 150
FEN = sys.argv[1]
MOVE = sys.argv[2]

#Check if postion is valid 
if not is_valid(FEN):
    print("This is not a chess position. Make sure your input is correct and try again.")
else:
    #Analyse position
    p = open_engine()
    analysis = analyse(p, FEN, NODES)
    close_engine(p)
    check = check_move(analysis, MOVE)
    #Check if move is legal
    if not check[0]:
        print("This move is not legal in the position. Make sure your input is correct and try again.")
    else:
        move = check[1]
        #Extract top 5 moves
        data = extract_data(analysis, move)
        #If move not in top 5 or less than 5 options, set to 0%.
        if (not data[0]):
            if data[1]==0: #less than 5 available moves
                print("Predicted probability of engine assistance: 50%")
            else: #not in top 5
                print("Predicted probability of engine assistance: 0%")
        #If all 5 options are equal - undecided.
        elif (analysis["V"] == 0.0).all():
            print("Predicted probability of engine assistance: 50%")
        else:
            #Run data through the model
            analysis = data[1]
            model = initialise_model()
            analysis = analysis['V'].values
            engine = run_model(model, analysis)
            print("Predicted probability of engine assistance: " + str(engine) +"%")