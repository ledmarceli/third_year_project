import chess
import chess.pgn
import pandas as pd
import torch

#Check if string is a FEN
def is_valid(fen_str):
    try:
        board = chess.Board(fen_str)
        return True
    except ValueError:
        return False

#Check if PGN is legitimate:
def check_pgn(pgn_name):
    try:
        pgn = open(pgn_name)
        game = chess.pgn.read_game(pgn)
        pgn.close()
        if game is not None and game.errors == [] and len(game.variations)>0:
            return True
        else:
            return False

    except chess.IllegalMoveError:
        return False

#Run the filtered lc0 judgements through the model
def run_model(model, array):
    input_tensor = torch.tensor(array)
    input_tensor = input_tensor.to(torch.float32)
    output_tensor = model(input_tensor)
    output_array = output_tensor.detach().numpy()
    engine = round(output_array[1]*100,2)
    return engine





