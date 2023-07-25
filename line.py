from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = [0]*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)
        
    # returns if two lines are parallel
    def is_parallel(self, line):
        vector = Vector(self.normal_vector)
        vector_1 = Vector(line.normal_vector)
        
        return vector.is_parallel(vector_1)
        
    # returns if two lines are equal by substituting same values of x & y in both line equations to see if same coordinates are produced
    def are_equal(self, line):
        if not self.is_parallel(line):
            return False
        
        vector = Vector(self.normal_vector)
        vector_1 = Vector(line.normal_vector)
        
        y_1 = round((self.constant_term - Decimal(self.normal_vector[0])) / Decimal(self.normal_vector[1]), 3)
        x_1 = round((self.constant_term - Decimal(self.normal_vector[1])) / Decimal(self.normal_vector[0]), 3)
        
        y_2 = round((line.constant_term - Decimal(line.normal_vector[0])) / Decimal(line.normal_vector[1]), 3)
        x_2 = round((line.constant_term - Decimal(line.normal_vector[1])) / Decimal(line.normal_vector[0]), 3)
        
        return [x_1, y_1] == [x_2, y_2]
      
    # returns if two lines are equal by checking if normal vector is orthogonal to vector between basepoints
    def are_equal_v2(self, line):
        if not self.is_parallel(line):
            return False
        
        x0 = self.basepoint
        y0 = line.basepoint
        
        basepoint_diff = x0.minus(y0)
        
        return basepoint_diff.is_orthogonal(Vector(self.normal_vector))
        
    # returns the intersection of two lines
    def find_intersection(self, line):
        if self.are_equal(line):
            return 'infinite intersections'
        elif self.is_parallel(line):
            return 'no intersection'
        
        a, b = self.normal_vector
        k_1 = self.constant_term
        c, d = line.normal_vector
        k_2 = line.constant_term
        
        x = round((Decimal(d)*k_1 - Decimal(b)*k_2) / Decimal(a*d - b*c), 3)
        y = round((Decimal(-c)*k_1 + Decimal(a)*k_2) / Decimal(a*d - b*c), 3)
        
        return Vector([x, y]) 


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


##################################
print('Intersections of Lines in 2D')

line = Line([4.046, 2.836], 1.21)
line_1 = Line([10.115, 7.09], 3.025)
print(line.is_parallel(line_1))
print(line.are_equal_v2(line_1))
print(line.find_intersection(line_1))

line = Line([7.204, 3.182], 8.68)
line_1 = Line([8.172, 4.114], 9.883)
print(line.is_parallel(line_1))
print(line.are_equal_v2(line_1))
print(line.find_intersection(line_1))

line = Line([1.182, 5.562], 6.744)
line_1 = Line([1.773, 8.343], 9.525)
print(line.is_parallel(line_1))
print(line.are_equal_v2(line_1))
print(line.find_intersection(line_1))