#VERSION AVEC SORTIES SUR TOUS LES MURS


#MODIFS : PLUS DE CASE DE DEPART AU 0, 0 MTN CEST 1, 0 OU 0, 1 AU MOINS
#MODIFS : IL Y A MTN DES SORTIES SUR LES COTES OUEST ET NORD
#MODIFS : DÉBUT D'UNE FONCTION EXPLORATEUR DU LABYRINTHE

import random
import os

# Créez un labyrinthe en utilisant l'algorithme de parcours en profondeur décrit à
# https://scipython.com/blog/making-a-maze/
# Christian Hill, avril 2017.

class Cell:
    """Une cellule dans le labyrinthe.

    Une cellule est un point dans la grille du labyrinthe, entouré par des murs dans
    les directions nord, est, sud ou ouest. Ces murs définissent la connectivité
    entre les cellules.
    """

    # Un dictionnaire indiquant les paires de murs opposés (nord-sud, est-ouest).
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialise une cellule à la position (x, y). Par défaut, tous ses murs sont présents."""
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}  # Toutes les directions ont des murs au départ.

        self.passage = 1
        self.chances = []

            
        
        self.infos = ["N : True", "E : True", "S : True", "W : True", 1, 1, "Passage : 0", 3, 0] # CS 04022025 Données d'information sur la cellule
                            # NESOPCA avec:
                            #   N: Nord     (Default: True) Si la valeur est 1 alors on a un mur au nord et 0 dans le cas contraire. Si on est déjà passé par ce mur la valeur est 2.
                            #   E: Est      (Default: True) Si la valeur est 1 alors on a un mur à l'est et 0 dans le cas contraire. Si on est déjà passé par ce mur la valeur est 2.
                            #   S: Sud      (Default: True) Si la valeur est 1 alors on a un mur au sud et 0 dans le cas contraire. Si on est déjà passé par ce mur la valeur est 2.
                            #   W: Ouest    (Default: True) Si la valeur est 1 alors on a un mur à l'ouest et 0 dans le cas contraire. Si on est déjà passé par ce mur la valeur est 2.
                            #   Coordonnée: x (Default: 1)
                            #   Coordonnée: y (Default: 1)
                            #   P: Passage  (Default: 0) Si la valeur est 1 alors on est déjà passé sur cette case
                            #   C: Chance   (Default: 3) Nombre de déplacement possibles non explorés. Au maximum on peut avoir 3 déplacements possibles, il faut au moins 1 mur.
                            #   A: Variable (Default: 0) Variable de test


    
    def set_passage(self, a):
        self.passage = a
        
        


    def get_chances(self):
        if self.walls['N'] == False :
            self.chances.append('N')
        if self.walls['E'] == False :
            self.chances.append('E')
        if self.walls['S'] == False :
            self.chances.append('S')
        if self.walls['W'] == False :
            self.chances.append('W')
        
        return self.chances
        




    def set_walls(self):
        if self.walls['N'] == False :
            self.infos[0] = "N : False"
        if self.walls['E'] == False :
            self.infos[1] = "E : False"
        if self.walls['S'] == False :
            self.infos[2] = "S : False"
        if self.walls['W'] == False :
            self.infos[3] = "W : False"
            
    
    def set_cos(self):        
        self.infos[4] = self.x
        self.infos[5] = self.y
        
            
        
        
    def has_all_walls(self):
        """Vérifie si la cellule possède encore tous ses murs (n'est pas encore connectée à d'autres)."""
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Supprime le mur entre la cellule courante (self) et une cellule voisine (other)."""
        self.walls[wall] = False  # Supprime le mur dans la direction spécifiée.
        other.walls[Cell.wall_pairs[wall]] = False  # Supprime le mur opposé dans la cellule voisine.


class Maze:
    """Représente un labyrinthe sous forme de grille de cellules."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialise une grille de labyrinthe avec nx colonnes et ny lignes.

        Le labyrinthe est construit à partir de la cellule initiale située
        aux coordonnées (ix, iy).
        """
        self.nx, self.ny = nx, ny  # Dimensions du labyrinthe.
        self.ix, self.iy = ix, iy  # Point de départ du labyrinthe.
        # Génère une grille de cellules (tableau 2D).
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        
        

    def cell_at(self, x, y):
        """Retourne la cellule située aux coordonnées (x, y)."""
        return self.maze_map[x][y]

    def open_exit(self):
        """Ouvre une sortie aléatoire sur l'un des quatre bords du labyrinthe."""
        # Choisir un côté au hasard
        side = random.choice(['N', 'S', 'E', 'W'])
        cordx = 0
        cordy = 0

        if side == 'N':  # Sortie au nord
            x = random.randint(1, self.nx - 1)
            self.cell_at(x, 0).walls['N'] = False  # Ouvrir le mur du nord pour une cellule sur le bord nord
            cordx = x
            cordy = 0
        elif side == 'S':  # Sortie au sud
            x = random.randint(0, self.nx - 1)
            self.cell_at(x, self.ny - 1).walls['S'] = False  # Ouvrir le mur du sud pour une cellule sur le bord sud
            cordx = x
            cordy = self.ny - 1
        elif side == 'E':  # Sortie à l'est
            y = random.randint(0, self.ny - 1)
            self.cell_at(self.nx - 1, y).walls['E'] = False  # Ouvrir le mur de l'est pour une cellule sur le bord est
            cordx = self.nx - 1
            cordy = y
        elif side == 'W':  # Sortie à l'ouest
            y = random.randint(1, self.ny - 1)
            self.cell_at(0, y).walls['W'] = False  # Ouvrir le mur de l'ouest pour une cellule sur le bord ouest
            cordx = 0
            cordy = y


        self.exitx=cordx
        self.exity=cordy
        


    def __str__(self):
        """Retourne une représentation textuelle simplifiée du labyrinthe."""
        maze_rows = ['-' * self.nx * 2]  # Ligne supérieure (mur horizontal).
        for y in range(self.ny):
            maze_row = ['|']  # Début de la ligne verticale.
            for x in range(self.nx):
                # Vérifie s'il y a un mur à l'est.
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']  # Ligne inférieure ou espace entre cellules.
            for x in range(self.nx):
                # Vérifie s'il y a un mur au sud.
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename):
        """Génère une image SVG du labyrinthe et l'enregistre dans un fichier."""

        aspect_ratio = self.nx / self.ny  # Rapport largeur/hauteur du labyrinthe.
        padding = 10  # Marge autour du labyrinthe.
        height = 500  # Hauteur en pixels.
        width = int(height * aspect_ratio)  # Largeur calculée en fonction du ratio.
        scy, scx = height / self.ny, width / self.nx  # Facteurs de mise à l'échelle.


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
            print(']]></style>\n</defs>', file=f)

            # Dessiner la cellule de départ en rouge à la position ix, iy
            start_x = self.ix * scx
            start_y = self.iy * scy
            print('<rect x="{}" y="{}" width="{}" height="{}" fill="red"/>'.format(
                start_x, start_y, scx, scy), file=f)

            # Dessiner la cellule d'arrivée en vert à la position exitx, exity
            # endx = self.exitx * scx
            # endy = self.exity *scy
            # print('<rect x="{}" y="{}" width="{}" height="{}" fill="green"/>'.format(
            # endx, endy, scx, scy, fill="green"), file=f)



            # Dessin des murs sud et est. et ouest et nord
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

                    if self.cell_at(x, y).walls['W']:
                        x1, y1, x2, y2 = x *scx, y *scy, x * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

                    if self.cell_at(x, y).walls['N']:
                        x1, y1, x2, y2 = x * scx, y * scy, (x + 1) * scx, y *scy
                        write_wall(f, x1, y1, x2, y2)


            # ce programme pour les murs N et W ne marche pas avec la sortie trouvée
            # Ajout des murs nord et ouest du bord du labyrinthe.
            #print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            #print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            #print('</svg>', file=f)




    def find_valid_neighbours(self, cell):
        """Trouve les voisins non visités de la cellule donnée."""
        delta = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]  # Directions possibles.
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):  # Vérifie si les coordonnées sont valides.
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():  # Vérifie si le voisin n'a pas encore été visité.
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        """Génère le labyrinthe en utilisant l'algorithme du parcours en profondeur."""
        n = self.nx * self.ny  # Nombre total de cellules.
        cell_stack = []  # Pile pour gérer les retours en arrière.
        current_cell = self.cell_at(self.ix, self.iy)  # Cellule de départ.
        nv = 1  # Nombre de cellules visitées.

        while nv < n:  # Tant que toutes les cellules ne sont pas visitées.
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # Impasse : retourne à la cellule précédente.
                current_cell = cell_stack.pop()
                continue

            # Choisit une cellule voisine au hasard et crée un passage.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1




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


# from df_maze import Maze

# # Maze dimensions (ncols, nrows)
# nx, ny = 15, 15
# # Maze entry position
# ix, iy = 0, 0

# maze = Maze(nx, ny, ix, iy)
# maze.make_maze()

# maze.open_exit()


    



# print(maze)

# # Change le répertoire courant pour correspondre au dossier contenant le script
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# print("Répertoire courant :", os.getcwd())

# maze.write_svg('maze.svg')



