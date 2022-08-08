from math import radians, cos, sin
import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

class Transform():
    
    def __init__(self, *args):
        super(Transform, self).__init__(*args)
        self.transformations = {
            'T': self.translate,
            'O': self.rotate,
            'C': self.scale,
            'S': self.shear,
            'R': self.reflect
        }
        self.N_2 = np.eye(3)
        self.N_3 = np.eye(4)
        self.transform()
        
    # Function to translate an object
    def translate(self):
        try:
            if len(self.M1[0]) == 3: #For 2D
                T = self.N_2
                # print(T)
                
                if self.Tx == '':
                    self.Tx = int(input("Enter the translation in x-direction: \n"))
                    self.Ty = int(input("Enter the translation in y-direction: \n"))
                    T[2][0] = self.Tx
                    T[2][1] = self.Ty
                else:
                    T[2][0] = self.Tx
                    T[2][1] = self.Ty
                    #     pass
            
            else: #For 3D
                T = self.N_3
                # print(T)
                
                if self.Tx == '':
                    self.Tx = int(input("Enter the translation in x-direction: \n"))
                    self.Ty = int(input("Enter the translation in y-direction: \n"))
                    self.Tz = int(input("Enter the translation in z-direction: \n"))
                    T[3][0] = self.Tx
                    T[3][1] = self.Ty
                    T[3][2] = self.Tz
                else:
                    T[3][0] = self.Tx
                    T[3][1] = self.Ty
                    T[3][2] = self.Tz
                    #     pass
        
        except:
            print('\nAn error occurred, try again. \n')
            self.translate()
        
        # print(T)
        return T.astype(np.int64)

    # Function to rotate an object about an origin or a point
    def rotate(self):
        tita = input("\nEnter the angle of rotation: \n(If clockwise, add a negative before the angle.) \n")
        try:
            tita = int(tita)
            costita = cos(radians(tita))
            sintita = sin(radians(tita))
            if len(self.M1[0]) == 3: #For 2D
                self.rot = input("\nDo you want to rotate about an arbitrary Point or an Origin? \n")
                self.rot = self.rot.capitalize()
                O = self.N_2
                # print('\n', O)
                O[0][0] = costita
                O[1][1] = costita
                O[0][1] = sintita
                O[1][0] = -sintita
                
                if self.rot == 'P':
                    self.cord = input("\nEnter the arbitrary point to rotate about: \n")
                    self.cord = self.cord.split(',')
                    for i in self.cord:
                        i = int(i)
                    
                    # self.cor = np.array[self.cord*len(self.M)]
                    # print(self.cord)
                    
                elif self.rot == 'O':
                    pass
            
            else: #For 3D
                O = self.N_3
                axis = input("Enter axis of rotation (X or Y or Z): \n")
                if axis.capitalize() == 'X':
                    O[1][1] = costita
                    O[2][2] = costita
                    O[1][2] = sintita
                    O[2][1] = -sintita
                elif axis.capitalize() == 'Y':
                    O[0][0] = costita
                    O[2][2] = costita
                    O[2][0] = sintita
                    O[0][2] = -sintita
                elif axis.capitalize() == 'Z':
                    O[0][0] = costita
                    O[1][1] = costita
                    O[0][1] = sintita
                    O[1][0] = -sintita
            
        except:
            print('An error occurred, try again.')
            self.rotate()
        
        # print(O)
        return O.astype(np.int64)

        

    # Function to scale an object's size
    def scale(self):
        try:
            if len(self.M1[0]) == 3: #For 2D
                C = self.N_2
                Cx = float(input("Enter the scale size in x-direction: \n"))
                Cy = float(input("Enter the scale size in y-direction: \n"))
                C[0][0] = Cx
                C[1][1] = Cy
                
            else: #For 3D
                C = self.N_3
                Cx = float(input("Enter the scale size in x-direction: \n"))
                Cy = float(input("Enter the scale size in y-direction: \n"))
                Cz = float(input("Enter the scale size in z-direction: \n"))
                C[0][0] = Cx
                C[1][1] = Cy
                C[2][2] = Cz
        except:
            print('An error occurred, try again.')
            self.scale()
        
        return C.astype(np.int64)
        

    # Function to shear an object
    def shear(self):
        
        try:
            if len(self.M1[0]) == 3: #For 2D
                S = self.N_2
                sh = input("\nEnter the shear parameter: \n")
                axis = input("\nEnter the direction of shear (y or x): \n")
                rel = input("\nIs the shear Relative to another line? (r or n): \n")
                sh = float(sh)
                if rel.capitalize() == 'R':
                    rel_para = input("Enter line parameter: \n")
                    rel_para = float(rel_para)
                    if axis.capitalize() == 'Y':
                        S[2][1] = -sh*rel_para
                    elif axis.capitalize() == 'X':
                        S[2][0] = -sh*rel_para
                elif rel.capitalize() == 'N':
                    pass
                
                if axis.capitalize() == 'Y':
                    S[0][1] = sh
                
                elif axis.capitalize() == 'X':
                    S[1][0] = sh
                    
            else: #For 3D
                S = self.N_3
                axis = input("\nEnter the direction of shear (y or x or z): \n")
                axes = ['X', 'Y', 'Z']
                axes.remove(axis)
                sh1 = int(input("Enter the shear in {}-direction".format(axes[0])))
                sh2 = int(input("Enter the shear in {}-direction".format(axes[1])))
                if axis.capitalize() == 'X':
                    S[0][1] = sh1
                    S[0][2] = sh2
                elif axis.capitalize() == 'Y':
                    S[1][0] = sh1
                    S[1][2] = sh2
                elif axis.capitalize() == 'Z':
                    S[2][0] = sh1
                    S[2][1] = sh2
                
        except:
            print('An error occured, try again!')
            self.shear()
        
        # print(S)
        return S.astype(np.int64)
            

    # Function to reflect an object
    def reflect(self):
        
        try:
            if len(self.M1[0]) == 3:
                R = self.N_2
                axis = input("Enter the axis to reflect about (X, Y, Origin, Line):\n")
                if axis.capitalize() == 'X':
                    R[1][1] = -1
                elif axis.capitalize() == 'Y':
                    R[0][0] = -1
                elif axis.capitalize() == 'O':
                    R[1][1] = -1
                    R[0][0] = -1
                elif axis.capitalize() == 'L':
                    ref = input("Enter the axis of the line to reflect (X, Y):\n")
                    if ref.capitalize() == 'X':
                        R[0][0] = 0
                        R[1][1] = 0
                        R[0][1] = 1
                        R[1][0] = 1
                    elif ref.capitalize() == 'Y':
                        R[0][0] = 0
                        R[1][1] = 0
                        R[0][1] = -1
                        R[1][0] = -1
            
            else:
                R = self.N_3
                plane = input("Enter the plane to reflect about (1-XY, 2-XZ, 3-YZ):\n")
                if int(plane) == 1:
                    R[2][2] = -1
                elif int(plane) == 2:
                    R[1][1] = -1
                elif int(plane) == 3:
                    R[0][0] = -1
                
        except:
            print('An exception occurred')
            self.reflect()
          
        return R.astype(np.int64)

    # Function to call any of the transformation above
    def transform(self):
        self.transform_list = []
        while True:
            transform = input('\nEnter the transformation you want to do: \nTranslate, rOtate, sCale, Shear, Reflect \nor Done when you are done or cLear to start again: \n').capitalize()
            if transform in self.transformations.keys():
                self.transform_list.append(transform)
            elif transform == "D":
                if len(self.transform_list) == 0:
                    print("\nYou have entered no transformation, try again.")
                    continue
                else:
                    break
            elif transform == 'L':
                self.transform()
            else:
                print("\nYou have entered an incorrect transformation, try again.")
                continue
        print(self.transform_list)
        self.point()
        
    # function to input coordinates
    def point(self):
        self.coordinates = []
        while True:
            coord = []
            coord_in = input("\nEnter the coordinates of the shape in the format (x,y) or 'D' when done or cLear to start again or Start again: \n")
            if coord_in == "":
                print("You have entered no coordinates, try again.")
                continue
            else:
                if str(coord_in).capitalize() == "D":
                    if len(self.coordinates) == 1 and len(self.transform_list) == 1 and self.transform_list[0] == 'T':
                        pass
                    elif len(self.coordinates) == 2:
                        pass
                    elif len(self.coordinates) > 2:
                        pass
                            # self.coordinates.append(self.coordinates[0])
                    else:
                        print('\nCannot transform a point, \nCheck transformation and points.')
                        self.transform()
                    break
                elif coord_in.capitalize() == "L":
                    self.point()
                elif coord_in.capitalize() == "S":
                    self.transform()
                else:
                    try:
                        coord_in = coord_in.split(',')
                        for i in range(0, len(coord_in)):
                            coord.append(int(coord_in[i]))
                        coord.append(1)
                        self.coordinates.append(list(coord))
                    except:
                        print('An error occured with the coordinates, try again.')
                        continue
        self.check_coordinates()
        
    # function to check coordinates validity
    def check_coordinates(self):
        check1 = len(self.coordinates[0])
        if check1 in range(3,5):
            for i in range(1, len(self.coordinates)):
                if check1 == len(self.coordinates[i]):
                    # print("Check {0} complete".format(i))
                    pass
                else:
                    print("Check {0} not complete".format(i))
                    print('The coordinates are not homogenous, \nInput the coordinates again.')
                    self.point()     
                break
        else:
            print("Can only transform in 2D and 3D, check coordinates.")
            self.point()
        print("\nCoordinates are Homogenous")
        self.transform_coordinates()
        
        
    def transform_coordinates(self):
        transformations_list = {
            'T': 'Translate',
            'O': 'Rotate',
            'C': 'Scale',
            'S': 'Shear',
            'R': 'Reflect'
        }
        self.Tx = ''
        self.Ty = ''
        self.M = np.array(self.coordinates)
        # self.M = np.transpose(self.M)
        self.M1 = self.M
        self.transformed_list = []
        for i in self.transform_list:
            M3 = self.transformations[i]()
            self.transformed_list.append(M3)
            # print(M3)
            if i == 'O':
                if self.rot == 'P':
                    self.Tx = self.cord[0]
                    self.Ty = self.cord[1]
                    print(self.Tx, self.Ty)
                    M4 = self.translate()
                    print('1\n',M4)
                    M2 = np.dot(self.M1, M4)
                    print('2\n',M2)
                    M2 = np.dot(M2, M3)
                    print('3\n',M2)
                    self.Tx = -int(self.cord[0])
                    self.Ty = -int(self.cord[1])
                    M5 = self.translate()
                    print('4\n',M5)
                    M6 = np.dot(M2, M5)
                    print('5\n',M6)
                    self.M1 = M6

                else:
                    self.M1 = np.dot(self.M1, M3)
            else:
                self.M1 = np.dot(self.M1, M3)
        # M1 = np.array(M1, np.int64)
        self.Tx = ''
        self.Ty = ''
        # self.M = np.delete(self.M, [-1], axis=1)
        # self.M1 = np.delete(self.M1, [-1], axis=1)
        if len(self.transform_list) == 1:
            print("\nYour Transformation is: ", transformations_list[self.transform_list[0]])
        else:
            print("\nYour Transformation(s) are: \n")
            for trans in range(0, len(self.transform_list)):
                print(transformations_list[self.transform_list[trans]])
        
        
        if len(self.M1[0]) == 3:
            X1 = self.M[:, 0]
            X1 = np.append(X1, X1[0])
            Y1 = self.M[:, 1]
            Y1 = np.append(Y1, Y1[0])
            X2 = self.M1[:, 0]
            X2 = np.append(X2, X2[0])
            Y2 = self.M1[:, 1]
            Y2 = np.append(Y2, Y2[0])
            plt.plot(X1, Y1, '-')
            plt.plot(X2, Y2, '--')
            plt.legend(['Original Shape', 'Transformed shape'])
            plt.show()
        else:
            # mpl.rcParams[‘legend.fontsize’] = 10
            fig = plt.figure()
            ax = fig.add_subplot(projection='3d')
            X1 = self.M[:, 0]
            X1 = np.append(X1, X1[0])
            Y1 = self.M[:, 1]
            Y1 = np.append(Y1, Y1[0])
            Z1 = self.M[:, 2]
            Z1 = np.append(Z1, Z1[0])
            X2 = self.M1[:, 0]
            X2 = np.append(X2, X2[0])
            Y2 = self.M1[:, 1]
            Y2 = np.append(Y2, Y2[0])
            Z2 = self.M1[:, 2]
            Z2 = np.append(Z2, Z2[0])
            ax.plot(X1, Y1, Z1)
            ax.plot(X2, Y2, Z2)
            
        
        
        '''
        print("\nYour coordinates are: \n", self.M)
        print("\nYour new coordinates after transformation are: \n", self.M1)
        print("\nYour transformation coordinates are: \n", self.transformed_list)
        '''

if __name__ == '__main__':
    Transform()
