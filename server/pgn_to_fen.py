import chess
import chess.pgn
import pandas as pd

#Returns all player's moves and postitions from the game
def get_moves_and_positions(pgn, player):
    game = chess.pgn.read_game(pgn)
    if game == None:
        return None
    #Finding the color the player plays
    if game.headers["White"] == player:
        color = True
    elif game.headers["Black"] == player:
        color = False
    else:
        print("ERROR: Player is not found in the PGN. Check if the name of the investigated player is correct.")
        exit()

    #Get all fen positions
    player_positions = []
    player_moves = []
    board = game.board()
    count = 0
    for move in game.mainline_moves():
        #Only look after the first 15 moves
        if count >30:
            if(board.turn == color):
                player_moves.append(chess.square_name(move.from_square) + chess.square_name(move.to_square))
            if (board.turn == color):
                player_positions.append(board.fen())
        board.push(move)
        count = count+1
    data = {"Position" : player_positions, "Move" : player_moves}
    df = pd.DataFrame(data = data)
    return df