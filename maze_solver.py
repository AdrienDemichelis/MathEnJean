### PROGRAMME DU MAZE SOLVER AVEC LA CLASSE CHEMIN = PILE


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




stack = [] # la pile
current_cell = solved_maze.cell_at(ix, iy) # current_cell est la cellule dans laquelle on se trouve, au départ, cest 0, 0 ou ix, iy
stack.append(current_cell)
directions = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]

while True:
    for exit, (dx, dy) in directions:
        if len(stack) != 1: 
            if current_cell.walls[exit] == False:
                    current_cell.walls[exit] = True # on met un mur pour ne plus revenir dans cette direction si elle ne marche pas
                    if current_cell.x + dx == nx or current_cell.y + dy == ny:
                        print('finished')
                        exit()
                    current_cell = maze.cell_at(current_cell.x + dx, current_cell.y + dy) #current_cell devient la cellule d'apres
                    current_cell.walls[current_cell.wall_pairs[exit]]
                    print('going', exit, current_cell.x, current_cell.y)
                    stack.append(current_cell)
                    print(current_cell.x, current_cell.y, current_cell.walls) # donne la liste des murs de la cellule dans laquelle on se trouve
                    break
        else:
            if current_cell.walls[exit] == False:
                    current_cell.walls[exit] = True # on met un mur pour ne plus revenir dans cette direction si elle ne marche pas
                    current_cell = maze.cell_at(current_cell.x + dx, current_cell.y + dy) #current_cell devient la cellule d'apres
                    current_cell.walls[current_cell.wall_pairs[exit]]
                    print('going', exit, current_cell.x, current_cell.y)
                    stack.append(current_cell)
                    print(current_cell.x, current_cell.y, current_cell.walls) # donne la liste des murs
                    break
    if current_cell.has_all_walls() == True:
        print(current_cell.x, current_cell.y, current_cell.walls) # donne la liste des murs
        current_cell = stack.pop()

















# class Chemin :
#     '''Fait une pile des cellules visitées, comme un chemin'''
    
#     def __init__(self, ix, iy):
#         self.this_cell = maze.cell_at(ix, iy)
#         self.stack = []
    
        
            

            
    
#     def push(self, cell):
#         '''Ajoute la cellule à la fin de la pile (= empile)'''
#         self.stack.append(cell)

#     def pop(self):
#         '''Supprime la cellule à la fin de la pile (= dépile)'''
#         self.stack.pop()



#     def créer_chemin(self):
#         self.push(self.this_cell) #cellule de départ
#         #directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] # N, E, S, W
#         self.switch_cell(self.this_cell)
        
        
#     def check_cell_in_stack(self, next_cell: Cell, coté, current_cell: Cell):
#         if next_cell in self.stack:
#             '''pour ne pas aller deux fois dans la meme direction'''
#             next_cell.chances.remove(coté)
#         else:
#             '''sinon ajouter a la pile la cellule courante'''
#             current_cell.chances.remove(coté)
#             self.push(next_cell)
            
            
            
        
#     '''passer d'une cellule a l'autre, si y a pas de mur qui les separe dans chacune des directions'''    
#     def switch_cell(self, current_cell: Cell):
#         self.print_cell(current_cell)
#         '''getchance: renvoi toutes les directions possible: sans mur'''
#         chances = current_cell.get_chances()
#         for coté in chances:
#             print(len(chances))
#             if coté == 'N':
#                 x = current_cell.x 
#                 y = current_cell.y - 1
#                 print('ligne 1')
                
#             if coté == 'E':
#                 x = current_cell.x + 1
#                 y = current_cell.y
#                 print('ligne 2')
    
#             if coté == 'S':
#                 x = current_cell.x 
#                 y = current_cell.y + 1
#                 print('ligne 3')
                
#             if coté == 'W':
#                 x = current_cell.x - 1
#                 y = current_cell.y
#                 print('ligne 4')

#             '''regarde si la cellule d';apres est deja dans le chemin: est-ce que je suis deja passe par la'''
#             self.check_cell_in_stack(maze.cell_at(x, y), coté, current_cell)
#             print('ligne 5')
#             self.switch_cell(maze.cell_at(x, y))

#     def print_cell(self, cell: Cell):
#         print("coucou", cell.x, cell.y)








# chemin = Chemin(ix, iy)


# chemin.créer_chemin()



# Change le répertoire courant pour correspondre au dossier contenant le script
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# print("Répertoire courant :", os.getcwd())

# maze.write_svg('maze.svg')
