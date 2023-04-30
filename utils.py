
GRID_SIZE = 5

# Datatype manipulation and representation

def stringToList(string):
    l = []
    for char in string:
        try:
            l.append(int(char))
        except ValueError:
            l.append(char)
    return l

def listToString(list):
    s = ''
    for item in list:
        s += str(item)
    return s

def listToMatrix(list):
    matrix = []
    for row in range(GRID_SIZE):
        matrix.append(list[row * GRID_SIZE:(row + 1) * GRID_SIZE])
    return matrix

def matrixToList(matrix):
    list = []
    for row in matrix:
        for item in row:
            list.append(item)
    return list

def printMatrix(matrix):
    for row in matrix:
        for item in row:
            print(f'[{str(item)}]', end='')
        print()
    print()

def ruleToString(condition, output):
    s = ''
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if condition[i][j]:
                s += '[#]'
            else:
                s += '[ ]'
        if i == 2:
            s += ' -> '
        else:
            s += '    '
        for j in range(GRID_SIZE):
            if output[i][j]:
                s += '[#]'
            else:
                s += '[ ]'
        s += '\n'
    return s

# Matrix transforms

# Rotates a matrix clockwise 90 degrees.
def rotate(matrix):
    new_matrix = [['#' for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            new_matrix[col][GRID_SIZE - 1 - row] = matrix[row][col]    
    return new_matrix

def getAllRotations(matrix):
    rotations = [matrix[:]]
    for count in range(3):
        rotations.append(rotate(rotations[count]))
    return rotations

def getAllMirrors(matrix):
    mirrors = [matrix[:]]
    mirrors.append(mirror(matrix, 'y'))
    mirrors.append(mirror(mirrors[0], 'x'))
    mirrors.append(mirror(mirrors[1], 'x'))
    return mirrors

# Mirrors a matrix along a given axis.
def mirror(matrix, axis):
    new_matrix = []
    if axis == 'x':
        for i in range(len(matrix) - 1, -1, -1):
            new_matrix.append(matrix[i])
    elif axis == 'y':
        for row in matrix:
            new_row = row[:]
            for i in range(int(GRID_SIZE / 2)):
                tmp = new_row[i]
                new_row[i] = new_row[GRID_SIZE - 1 - i]
                new_row[GRID_SIZE - 1 - i] = tmp
            new_matrix.append(new_row)
    return new_matrix

# Performs a translation transformation on a matrix.
# Note: All elements outside boundaries are replaced with 0's. Sign of dy is reversed.
def translate(matrix, dx, dy):
    filler = [0, 0, 0, 0, 0]
    def translateX(list, dx):
        if dx < 0:
            return list[-dx:] + filler[:-dx]
        elif dx > 0:
            return filler[:dx] + list[:-dx]
        else:
            return list[:]
    new_matrix = [translateX(row, dx) for row in matrix]
    if dy < 0:
        new_matrix = new_matrix[-dy:] + [filler for i in range(-dy)]
    elif dy > 0:
        new_matrix = [filler for i in range(dy)] + new_matrix[:-dy]
    return new_matrix

# Get all translations of output and respective condition
def getAllTranslations(condition, output):
    # Calculate translation limits
    min_x, max_x, min_y, max_y = GRID_SIZE, 0, GRID_SIZE, 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if output[y][x] == 1:
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
    min_dx = -min_x
    max_dx = GRID_SIZE - (max_x + 1)
    min_dy = -min_y
    max_dy = GRID_SIZE - (max_y + 1)
    # Get all translations within limits
    condition_translations, output_translations = [], []
    for dx in range(min_dx, max_dx + 1):
        for dy in range(min_dy, max_dy + 1):
            condition_translations.append(translate(condition, dx, dy))
            output_translations.append(translate(output, dx, dy))
    return condition_translations, output_translations

# Other Operations

def getNullMatrix():
    return [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

def listXOR(list_a, list_b):
    list_c = []
    for i in range(len(list_a)):
        list_c.append(list_a[i] ^ list_b[i])
    return list_c

# Performs an XOR operation on two matrices
# Assumes matrices are the same dimensions
def matrixXOR(matrix_a, matrix_b):
    matrix_c = []
    for i in range(len(matrix_a)):
        matrix_c.append(listXOR(matrix_a[i], matrix_b[i]))
    return matrix_c

def listAND(list_a, list_b):
    list_c = []
    for i in range(len(list_a)):
        list_c.append(list_a[i] & list_b[i])
    return list_c

def matrixAND(matrix_a, matrix_b):
    matrix_c = []
    for i in range(len(matrix_a)):
        matrix_c.append(listAND(matrix_a[i], matrix_b[i]))
    return matrix_c

def listOR(list_a, list_b):
    list_c = []
    for i in range(len(list_a)):
        list_c.append(list_a[i] | list_b[i])
    return list_c

def matrixOR(matrix_a, matrix_b):
    matrix_c = []
    for i in range(len(matrix_a)):
        matrix_c.append(listOR(matrix_a[i], matrix_b[i]))
    return matrix_c

# Other

def getUnique(list):
    unique = []
    for item in list:
        if item not in unique:
            unique.append(item[:])
    return unique

# Sort list_a and list_b (descending) according to list_b
def bubbleSortListPair(list_a, list_b):
    for i in range(len(list_b)):
        for j in range(len(list_b) - 1):
            if list_b[j] < list_b[j + 1]: # swap
                # list b
                list_b_tmp = list_b[j]
                list_b[j] = list_b[j + 1]
                list_b[j + 1] = list_b_tmp
                # list a
                list_a_tmp = list_a[j]
                list_a[j] = list_a[j + 1]
                list_a[j + 1] = list_a_tmp

def matrixCount(matrix, item):
    count = 0
    for row in matrix:
        count += row.count(item)
    return count

def matrixSum(matrix):
    return sum([sum(row) for row in matrix])

def getTransforms(condition, output):
        transforms, condition_transforms, output_transforms = [], [], []
        for rotation in getAllRotations(condition):
            condition_transforms += getAllMirrors(rotation)
        for rotation in getAllRotations(output):
            output_transforms += getAllMirrors(rotation)
        for i in range(len(output_transforms)):
            condition_transforms_translations, output_transforms_translations = getAllTranslations(condition_transforms[i], output_transforms[i])
            condition_transforms += condition_transforms_translations
            output_transforms += output_transforms_translations
        unique_output_transforms = []
        for i in range(len(output_transforms)):
            if output_transforms[i] not in unique_output_transforms:
                unique_output_transforms.append(output_transforms[i])
                transforms.append((condition_transforms[i], output_transforms[i]))
        return transforms

# 'centers' the 1s in a binary matrix
def toCenter(matrix):
    x_min, x_max = GRID_SIZE, 0
    y_min, y_max = GRID_SIZE, 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if matrix[y][x]:
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y
    dx = 2 - int((x_min + x_max) / 2)
    dy = 2 - int((y_min + y_max) / 2)
    return translate(matrix, dx, dy)

def areaOfEffect(output):
    up = translate(output, 0, -1)
    down = translate(output, 0, 1)
    left = translate(output, -1, 0)
    right = translate(output, 1, 0)
    return matrixOR(matrixOR(matrixOR(matrixOR(output, up), down), left), right)