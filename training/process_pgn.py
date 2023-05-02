import math
from pgn_to_fen import get_data_for_training
from analyse import analyse, open_engine, close_engine

#Driving code
FILE = "engine_games/TCEC_Season_14/TCEC_Season_14_full.pgn"
CSV = "datasets/computer.csv"
NODES = 150

#Make sure lc0 and python chess write castling the same way.
def check_move(df, move):
    if move not in df.index and move in ["e1g1", "e1c1", "e8g8", "e8c8"]:
        if(move == "e1g1" and "e1h1" in df.index):
            move = "e1h1"
        elif(move == "e1c1" and "e1a1" in df.index):
            move = "e1a1"
        elif(move == "e8c8" and "e8a8" in df.index):
            move = "e8a8"
        elif(move == "e8g8" and "e8h8" in df.index):
            move = "e8h8"
    return move

#Rounds up both positive and negative floats
def my_round(x):
    if x == 0:
        return 0
    else:
        return round(x, -int(math.floor(math.log10(abs(x)))) + (3))

#Gets the top 5 moves and calculates differences
def extract_data(analysis, move):
    if len(analysis.index)<5:
        return (False, 0)
    else:
        analysis = analysis.head(5).copy()
        analysis = analysis.fillna(-1)
        if move in analysis.index:
            value = analysis["V"][move]
            analysis["V"]=(analysis["V"]-value)
            analysis["V"] = analysis["V"].apply(my_round)
            return (True,analysis)
        else:
            return (False,1)

def process_pgn(file, csv, nodes):
    p = open_engine()
    csv = open(csv, "a")
    pgn = open(file, "r")
    game_count = 1
    out = []
    #While more games, continue analysing
    while True:
        df = get_data_for_training(pgn)
        if df is None:
            break
        else: 
            #Count games
            print("Game " + str(game_count))
            game_count = game_count + 1
            #Analyse
            for position, move in df.itertuples(index=False):
                analysis = analyse(p, position, nodes)
                move = check_move(analysis, move)
                data = extract_data(analysis, move)
                if data[0]:
                    line = ""
                    for value in data[1]["V"]:
                        line = line + str(value) + ","
                    line = line[:-1]
                    csv.write(line + "\n") 
    close_engine(p)
    pgn.close()
    csv.close()
    print("Processing Complete")


process_pgn(FILE, CSV, NODES)

