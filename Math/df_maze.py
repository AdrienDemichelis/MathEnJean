#VERSION AVEC SORTIES SUR TOUS LES MURS


#MODIFS : PLUS DE CASE DE DEPART AU 0, 0 MTN CEST 1, 0 AU MOINS
#MODIFS : IL Y A MTN DES SORTIES SUR LES COTES OUEST ET NORD

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
            y = random.randint(0, self.ny - 1)
            self.cell_at(0, y).walls['W'] = False  # Ouvrir le mur de l'ouest pour une cellule sur le bord ouest
            cordx = 0
            cordy = y
        

        self.exitx=cordx
        self.exity=cordy
        return cordx, cordy


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
            endx = self.exitx * scx
            endy = self.exity *scy
            print('<rect x="{}" y="{}" width="{}" height="{}" fill="green"/>'.format(
            endx, endy, scx, scy, fill="green"), file=f)



            # Dessin des murs sud et est.
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


            # ce programme pour les murs N et W ne marchent pas avec la sortie
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
            
            
    def find_exit(self):
        liste_cases = []
        
        # proceder par éliminations!!!

from df_maze import Maze

# Maze dimensions (ncols, nrows)
nx, ny = 15, 15
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.make_maze()


cox, coy = maze.open_exit()
print(cox, coy)


print(maze)

# Change le répertoire courant pour correspondre au dossier contenant le script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Répertoire courant :", os.getcwd())

maze.write_svg('maze.svg')




