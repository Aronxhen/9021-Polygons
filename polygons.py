class PolygonsError(Exception):
    def __inti__(self, input_error):
        self.input_error = input_error

er_language = 'Incorrect input.'
er_language2 = 'Cannot get polygons as expected.'
class Polygon:
    def __init__(self, figure_list):
        top_points = []

        for point in figure_list:
            last_index  = figure_list.index(point) - 1
            first_index = figure_list.index(point)
            second_index = (figure_list.index(point) + 1) % len(figure_list)

            last_direction = (figure_list[first_index][0] - figure_list[last_index][0], figure_list[first_index][1] - figure_list[last_index][1])
            next_direction = (figure_list[second_index][0] - figure_list[first_index][0], figure_list[second_index][1] - figure_list[first_index][1])

            if last_direction != next_direction:
                top_points.append(figure_list[first_index])

        self.figure = top_points
        self.caculate_perimeter()
        self.caculate_area()
        self.caculate_conves()
        self.caculate_rotation()

    def caculate_perimeter(self):
        normal = 0
        unnormal = 0
        for point in self.figure:
            first_index = self.figure.index(point) - 1
            second_index = self.figure.index(point)
            if self.figure[first_index][0] == self.figure[second_index][0]:
                x_diff = abs(self.figure[second_index][1] - self.figure[first_index][1])
                normal += abs(x_diff)
            elif self.figure[first_index][1] == self.figure[second_index][1]:
                y_diff = abs(self.figure[second_index][0] - self.figure[first_index][0])
                normal += abs(y_diff)
            else:
                y_diff = self.figure[second_index][0] - self.figure[first_index][0]
                unnormal += abs(y_diff)

        perimeter_part1 = normal * 0.4
        perimeter_part2 = unnormal

        if unnormal == 0:
            self.perimeter = str(round(perimeter_part1, 1))
        elif normal == 0:
            self.perimeter = str(perimeter_part2) + '*sqrt(.32)'
        else:
            self.perimeter = str(round(perimeter_part1, 1)) + ' + ' + str(perimeter_part2) + '*sqrt(.32)'

    def caculate_area(self):
        part = 0
        for (x0, y0), (x1, y1) in zip(self.figure, self.figure[1:] + [self.figure[0]]):
            part += (x0 * y1 - x1 * y0)
        self.area =  '{:.2f}'.format(abs(part) * 0.5 * 0.16)

    def caculate_conves(self):
        product_positive = []
        product_negative = []
        self.convex = 'yes'
        for point in self.figure:
            last_index  = self.figure.index(point) - 1
            first_index = self.figure.index(point)
            second_index = (self.figure.index(point) + 1) % len(self.figure)

            point_1 = self.figure[last_index]
            point_2 = self.figure[first_index]
            point_3 = self.figure[second_index]

            value_12 = (point_2[1] - point_1[1], point_2[0] - point_1[0])
            value_23 = (point_3[1] - point_2[1], point_3[0] - point_2[0])

            product = value_12[0] * value_23[1] - value_12[1] * value_23[0]

            if product_negative == [] and product > 0:
                product_positive.append(product)
            elif product_positive == [] and product < 0:
                product_negative.append(product)
            else:
                self.convex = 'no'
                break
    
    def abs_situation(self, mid_point, first_point, second_point):
        if not (abs(mid_point[1] - first_point[1]) == abs(mid_point[0] - second_point[0]) and abs(mid_point[0] - first_point[0]) == abs(second_point[1] - mid_point[1])):
            return False
        else:
            return True
        
    def caculate_rotation(self):
        if len(self.figure) % 2 == 1:
            self.rotation = '1'
            return

        mid_part = []
        first_part = []
        second_part = []

        for index1 in range (len(self.figure) // 2):
            first_part.append(self.figure[index1])
        for index2 in range(len(self.figure) // 2, len(self.figure)):
            second_part.append(self.figure[index2])

        for p1, p2 in zip(first_part, second_part):
            mid_point = ((p1[0] + p2[0]) / 2 , (p1[1] + p2[1]) / 2)
            mid_part.append(mid_point)

        if len(set(mid_part)) == 1:
            if len(self.figure) % 4 == 0:
                mid_point = mid_part[0]
                is_four = True
                for index1 in range (len(self.figure) // 4):
                    first_part.append(self.figure[index1])
                for index2 in range(len(self.figure) // 4, len(self.figure) // 4 * 2):
                    second_part.append(self.figure[index2])
                
                for first_point, second_point in zip(first_part, second_part):
                    is_four = self.abs_situation(mid_point, first_point, second_point)
                if is_four:
                    self.rotation = '4'
                    return
            self.rotation = '2'
        else:
            self.rotation = '1'


class Polygons:
    def __init__(self, file_name):
        with open(file_name) as file:
            grid = []
            for line in file:
                line = line.replace('\n','')
                line = line.replace(' ', '')
                new_line = list(line)
                grid.append(new_line)

        new_grid = self.create_newgrid(grid)
        self.x_long = len(new_grid[0])
        self.y_long = len(new_grid)
        self.grid = new_grid
        figures = []
        figures = self.get_list(figures)
        self.figures = figures
        self.find_depth()
        self.file_name = file_name


    def get_color(self):
        sorted_area = sorted(self.figures, key=lambda x: float(x.area), reverse=True)
        max_area = float(sorted_area[0].area)
        min_area = float(sorted_area[-1].area)
        for figure in sorted_area:
            if max_area == min_area:
                figure.color = 0
            else: 
                occ = max_area - float(figure.area)
                all_area = max_area - min_area
                figure.color = round(occ / all_area * 100)
            
    def display(self):
        self.get_color()
        sorted_depth = sorted(self.figures, key=lambda x: int(x.depth))
        tex_file_name = self.file_name.replace('.txt', '.tex')

        with open(tex_file_name, 'w') as file:
            file.write('\\documentclass[10pt]{article}\n\\usepackage{tikz}\n\\usepackage[margin=0cm]{geometry}')
            file.write('\n\\pagestyle{empty}\n\n')
            file.write('\\begin{document}\n')
            file.write('\n\\vspace*{\\fill}\n')
            file.write('\\begin{center}\n\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]')
            file.write('\n')
            file.write('\\draw[ultra thick] ')
            file.write(f'(0, 0) -- ({self.x_long - 1}, 0) -- ({self.x_long - 1}, {self.y_long - 1}) -- (0, {self.y_long - 1})')
            file.write(' -- cycle;\n\n')

            pre_depth = None
            for figure in sorted_depth:
                if figure.depth != pre_depth:
                    file.write(f'% Depth {figure.depth}\n')
                    pre_depth = figure.depth
                file.write(f'\\filldraw[fill=orange!{figure.color}!yellow] ')
                for point in figure.figure:
                    file.write(f'({point[1]}, {point[0]}) -- ')
                file.write('cycle;\n')
            file.write('\\end{tikzpicture}')
            file.write('\n\\end{center}\n')
            file.write('\\vspace*{\\fill}')
            file.write('\n\n\\end{document}\n')


    def analyse(self):
        for figure in self.figures:
            print('Polygon ' + str(self.figures.index(figure) + 1) + ':')
            print('    Perimeter: ' + figure.perimeter)
            print('    Area: ' + figure.area)
            print('    Convex: ' + figure.convex)
            print('    Nb of invariant rotations: ' + figure.rotation)
            print('    Depth: ' + figure.depth)
        

    def find_depth(self): 
        for index1 in range(len(self.figures)):
            depth = 0
            one_point = self.figures[index1].figure[0]
            for index2 in range(len(self.figures)):
                if index1 != index2:
                    is_contain = self.contain(one_point, self.figures[index2])
                    if is_contain:
                        depth += 1
            self.figures[index1].depth = str(depth)
    
    def caculate_x_coor(self, one_point, first_point, second_point):
        y1 = first_point[0] - second_point[0]
        y2 = first_point[1] - second_point[1]
        x = one_point[0] - first_point[0]
        slope = y1 / y2
        x_coor = x / slope
        answer = x_coor + first_point[1]
        return answer 

    def contain(self, one_point, one_figure):
        count = 0
        first_part = one_figure.figure
        second_part = one_figure.figure[1:] + [one_figure.figure[0]]

        for first_point, second_point in zip(first_part, second_part):
            y_situation = min(second_point[0], first_point[0]) < one_point[0] <= max(second_point[0], first_point[0])
            x_situation = one_point[1] <= max(second_point[1], first_point[1])
            if y_situation and x_situation:
                if first_point[1] == second_point[1]:
                    count += 1
                else:
                    x_coor = self.caculate_x_coor(one_point, first_point, second_point)
                    if one_point[1] <= x_coor:
                        count += 1
        if count % 2 == 1:
            return True
        else:
            return False

    def check_grid(self, new_grid, length):
        if not (2 <= len(new_grid) <= 50 and len(length) == 1):
            raise PolygonsError(er_language)
    def check_line(self, line):
        if line.count('0') + line.count('1') != len(line) or len(line) < 2 or len(line) > 50:
            raise PolygonsError(er_language)
        
    def create_newgrid(self, grid):
        new_grid = []
        length = set()
        for i in grid:
            if len(i) == 0:
                continue
            self.check_line(i)
            length.add(len(i))
            new_grid.append(i)
        self.check_grid(new_grid, length)

        return new_grid

    def change_figure(self, figure_list):
        for point in figure_list:
            self.grid[point[0]][point[1]] = '0'

    def change_equal(self, figure_list):
        max_index = len(figure_list) - 1
        for right in range(max_index):
            for left in range(max_index, right, -1):
                if figure_list[right] == figure_list[left]:
                    new_figure_list = figure_list[:right] + figure_list[left:]
                    return new_figure_list
    
        return figure_list
    
    def get_list(self, figures):
        for y in range(self.y_long):
            for x in range(self.x_long):
                if self.grid[y][x] == '1':
                    start_y = y
                    start_x = x
                    figure_list = self.find_figure(start_y, start_x)
                    figure_list = self.change_equal(figure_list)
                    self.change_figure(figure_list)
                    figures.append(Polygon(figure_list))
        return figures

    def find_figure(self, start_y, start_x):
        figure_list = [(start_y, start_x)]
        while True:
            point = self.find_next_point(figure_list)
            if point is False or point == (start_y, start_x):
                break
            figure_list.append(point)

        if point is False:
            raise PolygonsError(er_language2)
    
        return figure_list

    def find_next_point(self, figure_list):
        direction_dic = {0: (-1, 0), 1: (-1, 1), 2: (0, 1), 3: (1, 1), 4: (1, 0), 5: (1, -1), 6: (0 ,-1), 7: (-1 ,-1)}
        current_point = figure_list[-1]
        if len(figure_list) == 1:
            for i in direction_dic.keys():
                diff_y = direction_dic[i][0]
                diff_x = direction_dic[i][1]
                new_y = current_point[0] + diff_y
                new_x = current_point[1] + diff_x
                if 0 <= new_y < self.y_long and 0 <= new_x < self.x_long and self.grid[new_y][new_x] == '1':
                    new_point = (new_y, new_x)
                    return new_point
            return False
        
        else:
            pre_point = figure_list[-2]
            direct_y = current_point[0] - pre_point[0]
            direct_x = current_point[1] - pre_point[1]
            for key, value in direction_dic.items():
                if value == (direct_y, direct_x):
                    direction_index = key
                    break

            if direction_index == 0:
                direction_list = [6, 7, 0, 1, 2, 3]
            elif direction_index == 1:
                direction_list = [7, 0, 1, 2, 3, 4]
            elif direction_index == 2:
                direction_list = [0, 1, 2, 3, 4, 5]
            elif direction_index == 3:
                direction_list = [1, 2, 3, 4, 5, 6]
            elif direction_index == 4:
                direction_list = [2, 3, 4, 5, 6, 7]
            elif direction_index == 5:
                direction_list = [3, 4, 5, 6, 7, 0]
            elif direction_index == 6:
                direction_list = [4, 5, 6, 7, 0, 1]
            elif direction_index == 7:
                direction_list = [5, 6, 7, 0, 1, 2]

            for i in direction_list:
                diff_y = direction_dic[i][0]
                diff_x = direction_dic[i][1]
                new_y = current_point[0] + diff_y
                new_x = current_point[1] + diff_x
                if 0 <= new_y < self.y_long and 0 <= new_x < self.x_long and self.grid[new_y][new_x] == '1':
                    new_point = (new_y, new_x)
                    return new_point     
            return False

