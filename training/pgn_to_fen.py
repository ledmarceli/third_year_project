import chess
import chess.pgn
import pandas as pd

def get_data_for_training(pgn):
    game = chess.pgn.read_game(pgn)
    if game == None:
        return None

    #get all fen positions
    positions = []
    moves = []
    board = game.board()

    count = 0
    for move in game.mainline_moves():
        if(count>30):
            moves.append(chess.square_name(move.from_square) + chess.square_name(move.to_square))
            positions.append(board.fen())
        board.push(move)
        count = count+1

    data = {"Position" : positions, "Move" : moves}
    df = pd.DataFrame(data = data)
    return df