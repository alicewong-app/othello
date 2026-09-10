from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Game state constants
EMPTY = ' '
BLACK = 'B'
WHITE = 'W'

def reset_game():
    """Initializes an 8x8 Othello board and game state."""
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    # Starting 4 pieces in the center
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return {
        'board': board,
        'turn': BLACK,
        'winner': None
    }

# Global game state for simplicity (Use sessions/database for production)
game_state = reset_game()

# All 8 directions around a cell: (row_delta, col_delta)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def get_flips(board, row, col, player):
    """Returns a list of coordinate tuples that would be flipped if 'player' moves to (row, col)."""
    if board[row][col] != EMPTY:
        return []
        
    opponent = WHITE if player == BLACK else BLACK
    to_flip = []
    
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        direction_flips = []
        
        # Walk in this direction as long as we see the opponent's pieces
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            direction_flips.append((r, c))
            r += dr
            c += dc
            
        # If the walk ends on the current player's piece, the pieces in between are captured
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            to_flip.extend(direction_flips)
            
    return to_flip

def get_valid_moves(board, player):
    """Returns a set of (row, col) tuples where 'player' can legally move."""
    valid_moves = set()
    for r in range(8):
        for c in range(8):
            if get_flips(board, r, c, player):
                valid_moves.add((r, c))
    return valid_moves

@app.route('/')
def index():
    player_moves = get_valid_moves(game_state['board'], game_state['turn'])
    
    # Calculate scores
    black_score = sum(row.count(BLACK) for row in game_state['board'])
    white_score = sum(row.count(WHITE) for row in game_state['board'])
    
    return render_template('index.html', 
                           board=game_state['board'], 
                           turn=game_state['turn'], 
                           valid_moves=player_moves,
                           black_score=black_score,
                           white_score=white_score,
                           winner=game_state['winner'])

@app.route('/move', methods=['POST'])
def make_move():
    row = int(request.form.get('row'))
    col = int(request.form.get('col'))
    player = game_state['turn']
    
    flips = get_flips(game_state['board'], row, col, player)
    
    if flips:
        # Place the new piece
        game_state['board'][row][col] = player
        # Flip the captured pieces
        for r, c in flips:
            game_state['board'][r][c] = player
            
        # Switch turn to the next player
        next_player = WHITE if player == BLACK else BLACK
        
        # Check if the next player has any moves
        if get_valid_moves(game_state['board'], next_player):
            game_state['turn'] = next_player
        # If not, current player keeps playing if they have moves
        elif get_valid_moves(game_state['board'], player):
            pass 
        # Game over if neither player has moves
        else:
            black_score = sum(row.count(BLACK) for row in game_state['board'])
            white_score = sum(row.count(WHITE) for row in game_state['board'])
            if black_score > white_score:
                game_state['winner'] = 'Black Wins!'
            elif white_score > black_score:
                game_state['winner'] = 'White Wins!'
            else:
                game_state['winner'] = 'Tie Game!'
                
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global game_state
    game_state = reset_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
