import math
from pgn_to_fen import get_moves_and_positions
from analyse import analyse, open_engine, close_engine


#Ensures common castling notation between python chess and lc0
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
    if move not in df.index:
        return (False, move)
    else:
        return (True, move)

#Rounds both negative and positive floats
def my_round(x):
    if x == 0:
        return 0
    else:
        return round(x, -int(math.floor(math.log10(abs(x)))) + (3))

#Changes lc0 output to dataframe with 5 numbers.
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


def process_pgn(pgn, player):
    p = open_engine()
    nodes = 150
    engine_outputs = []
    game_count = 0
    #While there are games in the file, continue reading
    while True:
        df = get_moves_and_positions(pgn,player)
        if df is None:
            break
        else:
            #Label games
            game_count = game_count+1
            engine_outputs.append(game_count*100+1)
            #Analyse Moves
            for position, move in df.itertuples(index=False):
                analysis = analyse(p, position, nodes)
                move = check_move(analysis, move)[1]
                data = extract_data(analysis, move)
                if data[0]:
                    array = []
                    for value in data[1]["V"]:
                        array.append(value)
                    engine_outputs.append(array)
                ##If there are fewer than 5 moves available or the move not in top t5.
                elif data[1]==1:
                    engine_outputs.append(0)
                else:
                    engine_outputs.append(50)
    close_engine(p)
    pgn.close()
    return engine_outputs