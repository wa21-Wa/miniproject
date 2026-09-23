PIECES = ('P', 'B', 'R', 'Q')

ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
QUEEN_DIRECTIONS = ROOK_DIRECTIONS + BISHOP_DIRECTIONS


def to_grid(board):
    """Turn the board string into a list of lists of single characters,
    e.g. "R.\\n.K" -> [['R', '.'], ['.', 'K']]."""
    rows = board.split('\n')
    if rows and rows[-1] == '':
        rows = rows[:-1]
    return [list(row) for row in rows]


def is_valid_grid(grid):
    """Board must be a non-empty N x N square."""
    if not isinstance(grid, list) or len(grid) == 0:
        return False
    n = len(grid)
    for row in grid:
        if not isinstance(row, list) or len(row) != n:
            return False
    return True


def format_matrix(matrix):
    """Pretty-print a list of lists the way the screenshots show it:
    [['R', '.', '.', '.']
     ['.', '.', 'K', '.']
     ['P', '.', 'P', '.']
     ['.', '.', '.', '.']]"""
    n = len(matrix)
    lines = []
    for i, row in enumerate(matrix):
        text = str(row)
        prefix = '[' if i == 0 else ' '
        suffix = ']' if i == n - 1 else ''
        lines.append(prefix + text + suffix)
    return '\n'.join(lines)


def checkmate(board):
    """
    Debug-style version: prints the board, its shape, the squares every
    enemy piece can reach ("Check Range"), and finally Success/Fail.
    On undefined input (not a string, board not square) it stays silent.
    On an invalid number of Kings it prints the K-count error instead.
    """
    try:
        if not isinstance(board, str):
            return

        grid = to_grid(board)
        if not is_valid_grid(grid):
            print("Error: Board is not a square (N x N)")
            return

        n = len(grid)
        print(format_matrix(grid))
        print((n, n))

        king_positions = [
            (r, c) for r in range(n) for c in range(n) if grid[r][c] == 'K'
        ]
        if len(king_positions) != 1:
            print("Error: K Unit -> Possible Number")
            return
        king_pos = king_positions[0]

        threatened = set()
        is_check = False

        for r in range(n):
            for c in range(n):
                cell = grid[r][c]
                if cell not in PIECES:
                    continue

                if cell == 'P':
                    for target in ((r - 1, c - 1), (r - 1, c + 1)):
                        tr, tc = target
                        if 0 <= tr < n and 0 <= tc < n:
                            threatened.add(target)
                            if target == king_pos:
                                is_check = True
                    continue

                if cell == 'B':
                    directions = BISHOP_DIRECTIONS
                elif cell == 'R':
                    directions = ROOK_DIRECTIONS
                else:  # 'Q'
                    directions = QUEEN_DIRECTIONS

                for dr, dc in directions:
                    rr, cc = r + dr, c + dc
                    while 0 <= rr < n and 0 <= cc < n:
                        threatened.add((rr, cc))
                        if grid[rr][cc] != '.':
                            if (rr, cc) == king_pos:
                                is_check = True
                            break
                        rr += dr
                        cc += dc

        range_grid = [row[:] for row in grid]
        for (r, c) in threatened:
            if range_grid[r][c] == '.':
                range_grid[r][c] = 'X'

        print("Check Range:")
        print(format_matrix(range_grid))
        print("Success" if is_check else "Fail")
    except Exception as e:
        print("ERROR:", e)
        return