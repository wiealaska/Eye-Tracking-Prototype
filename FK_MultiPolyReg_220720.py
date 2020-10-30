import numpy as np
import os

SIZE = WIDTH, HEIGHT = 1512,1080

PATTERN3x3 = np.array([[1,0,0,1,0,0,1],
                       [0,0,0,0,0,0,0],
                       [1,0,0,1,0,0,1],
                       [0,0,0,0,0,0,0],
                       [1,0,0,1,0,0,1]])

PATTERN4x3 = np.array([[1,0,1,0,1,0,1],
                       [0,0,0,0,0,0,0],
                       [1,0,1,0,1,0,1],
                       [0,0,0,0,0,0,0],
                       [1,0,1,0,1,0,1]])

PATTERN7x5 = np.array([[1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1]])

# build an array containing the screen positions for the selected grid
def build_scheme(grid):
    scheme = []
    y = 0.5
    h = HEIGHT/len(grid)
    for row in grid:
        x = 0.5
        w = WIDTH/row
        for i in range(row):
            scheme.append([204+x*w, y*h])
            x += 1
        y += 1
    return scheme

SCREEN7x5 = build_scheme([7,7,7,7,7])

# poly_reg_2D can either be implemented as a method that does both polynomials (X(x,y) and Y(x,y)) automatically
# by calling itself with different parameters or it can be called twice, once for each screen coordinate
def poly_reg_2D(array, por, pg, xory, deg, deg2, all_data=False):
    """
Do a polynomial regression for x,y -> X or Y.

Param:
    array: array - Calibration template
    por: list - Point of Regard data (XY-data)
    pg: list - pupil glint data (xy-data)
    xory: int - X in terms of x and y or Y in terms of x and y
    deg: int - degree of polynomial
    
Returns:
    coeff: array - coefficiants for the polynomial
    """
    x = 0
    y = 1
    not_xory = y if xory == x else x
    n = 0
    
    pgGrid = np.zeros((len(array),len(array[0]), 2))
    porGrid = np.zeros((len(array),len(array[0]), 2))
    # fill the grids with the pg and por data
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] != 0:
                pgGrid[i][j]=pg[n]
                porGrid[i][j]=por[n]
            n+=1
    
    if xory == y:
        pgGrid = pgGrid.transpose(1, 0, 2)
        porGrid = porGrid.transpose(1, 0, 2)
        array = array.T
    
    print('The grid: \n', array)
    print('The pgGrid: \n', pgGrid)
    print('The porGrid: \n', porGrid)
    
    # array with deg+1 rows and len(grid) columns (len(grid) = amount of distinct Y/X pos, deg+1 = amount of coefs)
    arrCoeff_x = np.zeros((deg+1, len(array)))
    ai_x = []
    
    struct = []
    pg_X = []
    por_X = []
    pg_y = []
    i = 0
    
    # xory = 0: for every distinct value of Y a polynomial regression should be done for PGx and X
    # xory = 1: for every distinct value of X a polynomial regression shoudl be done for PGy and Y
    while i<len(array):
        j = 0
        pg_x = []
        por_x = []
        while j<len(array[i]):
            if array[i][j] != 0:
                pg_x.append(pgGrid[i][j][xory]) # enlists pg_x/pg_y values for a distinct Y/X 
                por_x.append(porGrid[i][j][xory]) # enlists por_x/pg_y values for a distinct Y/X
                pg_X.append(pgGrid[i][j][xory])  # for excel
                por_X.append(porGrid[i][j][xory])  # for excel
                pg_y.append(pgGrid[i][j][not_xory]) #enlists pg_y/pg_x in order of distinct Y/X
            j += 1
        # to get the grid structure pg_x length is stored in a list, e.g. struct = [3,4,3,4]
        struct.append(len(pg_x))
        print('Pg_x values for the', i+1, 'th distinct Y:', pg_x)
        print('Por_x values for the', i+1, 'th distinct Y:', por_x)
        if len(pg_x) > 0: # not really neccesary
            coeff = np.polyfit(pg_x, por_x, deg)
            print('Coefficiants for', i+1, 'th distinct Y position:', coeff)
            n = 0
            # store the coefficiants in arrCoeff
            while n < len(arrCoeff_x):
                arrCoeff_x[n][i]=coeff[n]
                n += 1
        i += 1
    # coefficiants in terms of pg_y
    n=0
    print('arrCoeff_x:', arrCoeff_x)
    print('Grid structure:', struct)
    print('Pg_y for a_i:', pg_y)
    while n <= deg:
        coeff_xi = []
        m = 0
        while m < len(arrCoeff_x[n]):  
            for i in range(struct[m]):
                coeff_xi.append(arrCoeff_x[n][m])
            m +=1
        print('a', n+1, ':', coeff_xi)        
        
        # pg_y -> coeff_xi
        coeff = np.polyfit(pg_y, coeff_xi, deg2)
        print('Coefficiants for a',n, ':', coeff)
        #for i in range(len(coeff)):
        ai_x.append(coeff)
        n += 1
        
    if all_data == True:
        return pg_X, por_X, pg_y, arrCoeff_x
    return ai_x

if __name__ == "__main__":
    
    # loading the data of pupil glint vector
    directory = 'C:/Users/ZVSL/Desktop/Franziska/Study2/EyeFeatures/Vector'
    pgfile = 'pg_FK_cal7x5_eyemark_blur_left_rep1.dat' 
    filepath = directory + '/' + pgfile
    data = np.loadtxt(filepath)
    #print('PG: \n', data)
    pg = data  # normalized pupil glint vector data

    pattern = PATTERN3x3
    screen = SCREEN7x5 # point of regard // calibration screen used
    # X(x,y)
    coeffX = poly_reg_2D(pattern, screen, pg, 0, 1, 1)

    # same procedure for Y(x,y) with different degrees for polyfit 
    coeffY = poly_reg_2D(pattern, screen, pg, 1, 1, 1)

    print('coefficiants X:', coeffX)
    #print(coeffY)

    # Test the polynomial
    for i in range(len(pg)):
        x = pg[i][0]
        y = pg[i][1]
        X = coeffX[0]*x**3*y+coeffX[1]*x**3+coeffX[2]*x**2*y+coeffX[3]*x**2+coeffX[4]*x*y+coeffX[5]*x+coeffX[6]*y+coeffX[7]
        Y = coeffY[0]*x**2*y**2+coeffX[1]*x*y**2+coeffX[2]*x*y**2+coeffX[3]*x**2+coeffX[4]*x*y+coeffX[5]*x+coeffX[6]*y+coeffX[7]
        print(X, Y)
