from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# FIXED: Hardcoded fallback key ensures you aren't kicked out of the game when Flask reloads code
app.secret_key = os.environ.get('SECRET_KEY', 'othello_secret_dev_key_123')

# Initial board state function to easily reset
def get_initial_board():
    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3], board[3][4], board[4][3], board[4][4] = 1, -1, -1, 1
    return board

def flip_tiles(board, x, y, player):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        if 0 <= x + dx < 8 and 0 <= y + dy < 8 and board[x + dx][y + dy] == -player:
            tiles_to_flip = []
            i, j = x + dx, y + dy
            while 0 <= i < 8 and 0 <= j < 8 and board[i][j] == -player:
                tiles_to_flip.append((i, j))
                i += dx
                j += dy
            if 0 <= i < 8 and 0 <= j < 8 and board[i][j] == player:
                for tx, ty in tiles_to_flip:
                    board[tx][ty] = player

def is_valid_move(board, x, y, player):
    if board[x][y] != 0:
        return False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        i, j = x + dx, y + dy
        if 0 <= i < 8 and 0 <= j < 8 and board[i][j] == -player:
            while 0 <= i < 8 and 0 <= j < 8 and board[i][j] == -player:
                i += dx
                j += dy
            if 0 <= i < 8 and 0 <= j < 8 and board[i][j] == player:
                return True
    return False

# Helper to check if a player has *any* legal moves left on the board
def has_valid_moves(board, player):
    for r in range(8):
        for c in range(8):
            if is_valid_move(board, r, c, player):
                return True
    return False

@app.route('/')
def index():
    # Initialize game state in user session if it doesn't exist
    if 'board' not in session:
        session['board'] = get_initial_board()
        session['current_player'] = 1  # 1 = Black, -1 = White
        session['game_over'] = False
        session['winner'] = ""

    board = session['board']
    
    # Calculate scores
    black_score = sum(row.count(1) for row in board)
    white_score = sum(row.count(-1) for row in board)

    return render_template(
        'index.html', 
        board=board, 
        current_player=session['current_player'],
        black_score=black_score,
        white_score=white_score,
        game_over=session.get('game_over', False),
        winner=session.get('winner', "")
    )

@app.route('/play', methods=['POST'])
def play():
    if 'board' not in session or session.get('game_over', False):
        return redirect(url_for('index'))

    # FIXED: Deep-copy the board array out of the session to ensure updates register correctly
    board = [list(row) for row in session['board']]
    player = session['current_player']

    x = int(request.form['x'])
    y = int(request.form['y'])

    if is_valid_move(board, x, y, player):
        board[x][y] = player
        flip_tiles(board, x, y, player)
        
        next_player = -player
        
        # Check for valid moves to see if game continues
        if has_valid_moves(board, next_player):
            player = next_player
        elif not has_valid_moves(board, player):
            # GAME OVER: Neither player has legal moves left
            session['game_over'] = True
            
            # Count final pieces to determine the winner
            black_score = sum(row.count(1) for row in board)
            white_score = sum(row.count(-1) for row in board)
            
            if black_score > white_score:
                session['winner'] = "Black Wins!"
            elif white_score > black_score:
                session['winner'] = "White Wins!"
            else:
                session['winner'] = "It's a Tie!"
        
        # FIXED: Reassign the completely new copy back to the session block
        session['board'] = board
        session['current_player'] = player
        session.modified = True

    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('board', None)
    session.pop('current_player', None)
    session.pop('game_over', None)
    session.pop('winner', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
