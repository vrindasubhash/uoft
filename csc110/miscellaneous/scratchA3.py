for i in range(0, num_points - 1):
    if i in [0, 1] or vertex_indexes[i - 1] != vertex_indexes[i - 2]:
        n = random.randint(0, len(vertex_points) - 1)
        vertex_indexes.append(n)
        point = current_point
        vertex = vertex_points[n]
        x = (point[0] + vertex[0]) // 2
        y = (point[1] + vertex[1]) // 2
        a3_helpers.draw_pixel(pygame_screen, current_point, (255, 91, 165))
        current_point = (x, y)
    else:
        illegal_index = [vertex_indexes[i - 1]]
        if illegal_index == 0:
            illegal_index.append(1)
            illegal_index.append(len(vertex_points) - 1)

        elif illegal_index == len(vertex_points) - 1:
            illegal_index.append(0)
            illegal_index.append(len(vertex_points) - 2)

        else:
            illegal_index.append(vertex_indexes[i - 1] + 1)
            illegal_index.append(vertex_indexes[i - 1] - 1)

        legal = legal_indexes(illegal_index, len(vertex_points))
        n = random.randint(0, len(legal) - 1)
        n_legal = legal[n]
        vertex_indexes.append(n_legal)
        point = current_point
        vertex = vertex_points[n_legal]
        x = (point[0] + vertex[0]) // 2
        y = (point[1] + vertex[1]) // 2
        a3_helpers.draw_pixel(pygame_screen, current_point, (255, 91, 165))
        current_point = (x, y)
