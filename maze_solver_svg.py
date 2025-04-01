### PROGRAMME DU MAZE SOLVER AVEC LA PILE


import os
from df_maze import Maze
import copy







# Maze dimensions (ncols, nrows)
nx, ny = 15, 15
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()
maze.open_exit()

print(maze)

# Change le répertoire courant pour correspondre au dossier contenant le script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


maze.write_svg('maze.svg')


solved_maze = copy.deepcopy(maze)





def write_solution_svg(filename):
        """Génère une image SVG du labyrinthe et l'enregistre dans un fichier."""

        aspect_ratio = nx / ny  # Rapport largeur/hauteur du labyrinthe.
        padding = 10  # Marge autour du labyrinthe.
        height = 500  # Hauteur en pixels.
        width = int(height * aspect_ratio)  # Largeur calculée en fonction du ratio.
        scy, scx = height / ny, width / nx  # Facteurs de mise à l'échelle.


        def write_wall(f, x1, y1, x2, y2):
            """Écrit une ligne représentant un mur dans le fichier SVG."""
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2), file=f)

        # Écriture du fichier SVG.
        with open(filename, 'w') as f:
            # En-tête SVG et styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'.format(
                width + 2 * padding, height + 2 * padding, -padding, -padding, width + 2 * padding, height + 2 * padding), file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n', file=f)
            # on définie ci-dessous la tête d'une flèche (on est tjs dans <defs>)
            print('<marker id="head" orient="auto" markerWidth="3" markerHeight="4" refX="0.1" refY="2">\n', file=f)
            print('<path d="M0,0 V4 L2,2 Z" fill="red" />\n', file=f)
            print('</marker>\n</defs>\n', file=f)

            for x in range(nx):
                for y in range(ny):
                    if solved_maze.cell_at(x, y) in stack:
                        this_cell = solved_maze.cell_at(x, y)
                        if this_cell != stack[0]: # vérifie qu'on est pas dans la dernière dellule du stack, si oui : il y a plus de flèche à écrire
                            next_cell = stack[stack.index(this_cell) - 1]
                            '''
                            pour avoir la direction dans laquelle la flèche pointe, on regarde la cellule d'avant dans le stack
                            et la direction qu'on a pris depuis pour arriver à this_cell, c'est la direction de notre flèche.
                            - 1 : c'est l'index de la cellule d'avant.
                            stack.index(this_cell) : cela nous renvoie l'index de la cellule dans laquelle nous sommes
                            '''
                            dif = (this_cell.x - next_cell.x, this_cell.y - next_cell.y) # on prend la différence des coordonnées entre les deux cellules
                            for exit, (dx, dy) in directions:
                                if dif[0] == dx and dif[1]== dy:
                                    sortie = exit
                            if sortie == 'E': 
                                print(f'<path marker-end="url(#head)" stroke-width="4" stroke="red" d="M {(x * scx)+5},{(y * scy)+scy/2} {(x * scx)+scx-10},{(y * scy)+scy/2}" />', file=f)
                            if sortie == 'W': 
                                print(f'<path marker-end="url(#head)" stroke-width="4" stroke="red" d="M {(x * scx)+scx-5},{(y * scy)+scy/2} {(x * scx)+10},{(y * scy)+scy/2}" />', file=f)
                            if sortie == 'S': 
                                print(f'<path marker-end="url(#head)" stroke-width="4" stroke="red" d="M {(x * scx)+scx/2},{(y * scy)+5} {(x * scx)+scx/2},{(y * scy)+scy-10}" />', file=f)
                            if sortie == 'N': 
                                print(f'<path marker-end="url(#head)" stroke-width="4" stroke="red" d="M {(x * scx)+scx/2},{(y * scy)+scy-10} {(x * scx)+scx/2},{(y * scy)+10}" />', file=f)
                            '''                                                                          |                                  |  |                              |
                                                                                                            = coordonnées x, y de mon point      coordonnées du point d'arrivée  
                                                                                                            de départ de la ligne                x, y de la ligne
                                "M x,y x,y" signifie 'move' = crée une ligne avec un point de 
                                départ et un point d'arrivée'''                



            # Dessin des murs sud et est. et ouest et nord
            for x in range(nx):
                for y in range(ny):
                    if maze.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if maze.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

                    if maze.cell_at(x, y).walls['W']:
                        x1, y1, x2, y2 = x *scx, y *scy, x * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

                    if maze.cell_at(x, y).walls['N']:
                        x1, y1, x2, y2 = x * scx, y * scy, (x + 1) * scx, y *scy
                        write_wall(f, x1, y1, x2, y2)
                    '''
                    Ci-dessus, il faut utiliser maze.cell_at() et non pas solved_maze.cell_at() car
                    les murs des cellules de solved_maze sont modifiés
                    '''
                    
            # Dessiner la cellule de départ en rouge à la position ix, iy
            start_x = ix + 2
            start_y = iy + 2
            print('<rect x="{}" y="{}" width="{}" height="{}" fill="red"/>'.format(
                start_x, start_y, scx - 4, scy - 4), file=f)







stack = [] # la pile
current_cell = solved_maze.cell_at(ix, iy) # current_cell est la cellule dans laquelle on se trouve, au départ, cest 0, 0 ou ix, iy
# stack.append(current_cell)
directions = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]

while True:
    for exit, (dx, dy) in directions:
        if current_cell.walls[exit] == False:
            current_cell.walls[exit] = True # on met un mur pour ne plus revenir dans cette direction si elle ne marche pas
            stack.append(current_cell) # je mets la cellule avec le nouveau mur
            if current_cell.x + dx == nx or current_cell.y + dy == ny or current_cell.x + dx == ix - 1 or current_cell.y + dy == iy - 1:
                print("finished")
                for i in range(len(stack)):
                    print(stack[i].x, stack[i].y)
                write_solution_svg('solution.svg') # on crée le svg de la solution
                os._exit(0) # on sort de la boucle while True
            current_cell = solved_maze.cell_at(current_cell.x + dx, current_cell.y + dy) # current_cell devient la cellule d'apres
            current_cell.walls[current_cell.wall_pairs[exit]] = True # il faut empêcher de revenir dans la cellule d'avant, murs opposes de la cellule d'après
            print('going', exit, current_cell.x, current_cell.y) 
            # stack.append(current_cell)
            print(current_cell.x, current_cell.y, current_cell.walls) # donne la liste des murs de la cellule dans laquelle on se trouve
            break
    if current_cell.has_all_walls() == True:
        print("popping", current_cell.x, current_cell.y, current_cell.walls) # donne la liste des murs
        current_cell = stack.pop()


