def main():
    quoridor = Quoridor()
    quoridor.read_board(console=False)
    board = quoridor.board.copy()
    (x, y) = quoridor.get_player_pos()
    possible_moves = quoridor.get_all_possible_moves(x, y, quoridor.enemy_pos, board)
    board = [
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 9, 9, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    path_finding = PathFinding(5)
    path_finding.update_board(board)
    path_finding.set_entity(0, 4, 8, 2)
    path, player = path_finding.a_star()
    current = path_finding.last

    while current != None:
        print(current)
        current = current.parent

    print(path, player)
    for move, player, enemy in possible_moves:
        print(f"""
        Move: {move}
        Player distance: {player}
        Enemy distance: {enemy}""")

        if move.move == "L":
            board[x][y] = 0
            board[move.x][move.y] = 1
            print()
            for i in range(2 * quoridor.n - 1):
                for j in range(2 * quoridor.n - 1):
                    print(board[i][j], end=" ")
                print()
            print()
            board[x][y] = 1
            board[move.x][move.y] = 0
        else:
            mid_x = (move.x + move.wx) // 2
            mid_y = (move.y + move.wy) // 2
            board[move.x][move.y] = 9
            board[move.wx][move.wy] = 9
            board[mid_x][mid_y] = 9
            print()
            for i in range(2 * quoridor.n - 1):
                for j in range(2 * quoridor.n - 1):
                    print(board[i][j], end=" ")
                print()
            print()

            board[move.x][move.y] = 0
            board[move.wx][move.wy] = 0
            board[mid_x][mid_y] = 0
    start = time.time()
    label, best_move = quoridor.min_max(board, True, quoridor.player_pos, quoridor.enemy_pos,
                                       quoridor.player_walls, quoridor.enemy_walls, max_depth=4)
    end = time.time()

    print("Time taken:", end - start)
    print(label, best_move)

    quoridor = Quoridor()
    quoridor.read_board(console=False)
    board = quoridor.board.copy()
    (x, y) = quoridor.get_player_pos()

    quoridor.player_walls = quoridor.m
    quoridor.enemy_walls = quoridor.m

    start = time.time()
    label, best_move = quoridor.min_max(board, True, quoridor.player_pos, quoridor.enemy_pos,
                                        quoridor.player_walls, quoridor.enemy_walls, max_depth=5)
    end = time.time()

    print("Time taken:", end - start)
    print(label, best_move)