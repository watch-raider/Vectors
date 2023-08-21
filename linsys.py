from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        # add your code here
        item1 = self.__getitem__(row1)
        item2 = self.__getitem__(row2)
        self.__setitem__(row1, item2)
        self.__setitem__(row2, item1)


    def multiply_coefficient_and_row(self, coefficient, row):
        # add your code here
        p = self.__getitem__(row)
        n = Vector(p.normal_vector)
        c = p.constant_term
        
        n_result = n.multiply(coefficient)
        c_result = c*coefficient
        p_result = Plane(normal_vector=list(n_result.coordinates), constant_term=c_result)
        
        self.__setitem__(row, p_result)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        # add your code here
        p = self.__getitem__(row_to_add)
        n = Vector(p.normal_vector)
        c = p.constant_term
        n = n.multiply(coefficient)
        c = c*coefficient
        
        p1 = self.__getitem__(row_to_be_added_to)
        n1 = Vector(p1.normal_vector)
        c1 = p1.constant_term
        
        n_result = n1.plus(n)
        c_result = c+c1
        
        p_result = Plane(normal_vector=list(n_result.coordinates), constant_term=c_result)
        
        self.__setitem__(row_to_be_added_to, p_result)
        
    def compute_triangular_form(self):
        system = deepcopy(self)
        
        num_eqs = len(system)
        num_vars = system.dimension
        
        j = 0 
        
        for i in range(num_eqs):
            
            while j < num_vars:
                c = MyDecimal(system[i].normal_vector[j])
                if c.is_near_zero():
                    swap_succeeded = system.swap_for_nonzero_coefficient_eq(i, j)
                    if not swap_succeeded:
                        j += 1
                        continue
                
                system.clear_coefficients_below(i, j)
                j += 1
                break
        
        return system
                
    def swap_for_nonzero_coefficient_eq(self, row, col):
        num_eqs = len(self)
         
        for k in range(row + 1, num_eqs):
            coefficient = MyDecimal(self[k].normal_vector[col])
            if not coefficient.is_near_zero():
                self.swap_rows(row, k)
                return True
        
        return False
        
    def clear_coefficients_below(self, row, col):
        num_eqs = len(self)
        beta = MyDecimal(self[row].normal_vector[col])
        
        for k in range(row + 1, num_eqs):
            n = self[k].normal_vector
            gamma = MyDecimal(n[col])
            alpha = -gamma/beta
            self.add_multiple_times_row_to_row(alpha, row, k)


    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e


        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


# p0 = Plane(normal_vector=[1,2,1], constant_term=5)
# p1 = Plane(normal_vector=[0,1,0], constant_term=2)
# p2 = Plane(normal_vector=[1,1,-1], constant_term=3)
# p3 = Plane(normal_vector=[1,0,-2], constant_term=2)

# s = LinearSystem([p0,p1,p2,p3])

# print(s.indices_of_first_nonzero_terms_in_each_row())
# print('{},{},{},{}'.format(s[0],s[1],s[2],s[3]))
# print(len(s))
# print(s)

# s[0] = p1
# print(s)

# print(MyDecimal('1e-9').is_near_zero())
# print(MyDecimal('1e-11').is_near_zero())


#p0 = Plane(normal_vector=[1,1,1], constant_term=1)
#p1 = Plane(normal_vector=[0,1,0], constant_term=2)
#p2 = Plane(normal_vector=[1,1,-1], constant_term=3)
#p3 = Plane(normal_vector=[1,0,-2], constant_term=2)
#
#s = LinearSystem([p0,p1,p2,p3])
#s.swap_rows(0,1)
#if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
#    print('test case 1 failed')
#
#s.swap_rows(1,3)
#if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
#    print('test case 2 failed')
#
#s.swap_rows(3,1)
#if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
#    print('test case 3 failed')
#
#s.multiply_coefficient_and_row(1,0)
#if not (str(s[0]) == str(p1) and s[1] == p0 and s[2] == p2 and s[3] == p3):
#    print('test case 4 failed')
#
#s.multiply_coefficient_and_row(-1,2)
#if not (str(s[0]) == str(p1) and
#        str(s[1]) == str(p0) and
#        str(s[2]) == str(Plane(normal_vector=[-1,-1,1], constant_term=-3)) and
#        str(s[3]) == str(p3)):
#    print('test case 5 failed')
#
#s.multiply_coefficient_and_row(10,1)
#if not (str(s[0]) == str(p1) and
#        str(s[1]) == str(Plane(normal_vector=[10,10,10], constant_term=10)) and
#        str(s[2]) == str(Plane(normal_vector=[-1,-1,1], constant_term=-3)) and
#        str(s[3]) == str(p3)):
#    print('test case 6 failed')
#
#s.add_multiple_times_row_to_row(0,0,1)
#if not (str(s[0]) == str(p1) and
#        str(s[1]) == str(Plane(normal_vector=[10,10,10], constant_term=10)) and
#        str(s[2]) == str(Plane(normal_vector=[-1,-1,1], constant_term=-3)) and
#        str(s[3]) == str(p3)):
#    print('test case 7 failed')
#
#s.add_multiple_times_row_to_row(1,0,1)
#if not (str(s[0]) == str(p1) and
#        str(s[1]) == str(Plane(normal_vector=[10,11,10], constant_term=12)) and
#        str(s[2]) == str(Plane(normal_vector=[-1,-1,1], constant_term=-3)) and
#        str(s[3]) == str(p3)):
#    print('test case 8 failed')
#
#s.add_multiple_times_row_to_row(-1,1,0)
#if not (str(s[0]) == str(Plane(normal_vector=[-10,-10,-10], constant_term=-10)) and
#        str(s[1]) == str(Plane(normal_vector=[10,11,10], constant_term=12)) and
#        str(s[2]) == str(Plane(normal_vector=[-1,-1,1], constant_term=-3)) and
#        str(s[3]) == str(p3)):
#    print('test case 9 failed')

# p1 = Plane(normal_vector=[1,1,1], constant_term=1)
# p2 = Plane(normal_vector=[0,1,1], constant_term=2)
# s = LinearSystem([p1,p2])
# t = s.compute_triangular_form()
# if not (str(t[0]) == str(p1) and
        # str(t[1]) == str(p2)):
    # print('test case 1 failed')

# p1 = Plane(normal_vector=[1,1,1], constant_term=1)
# p2 = Plane(normal_vector=[1,1,1], constant_term=2)
# s = LinearSystem([p1,p2])
# t = s.compute_triangular_form()
# if not (str(t[0]) == str(p1) and
        # str(t[1]) == str(Plane(constant_term=1))):
    # print('test case 2 failed')

# p1 = Plane(normal_vector=[1,1,1], constant_term=1)
# p2 = Plane(normal_vector=[0,1,0], constant_term=2)
# p3 = Plane(normal_vector=[1,1,-1], constant_term=3)
# p4 = Plane(normal_vector=[1,0,-2], constant_term=2)
# s = LinearSystem([p1,p2,p3,p4])
# t = s.compute_triangular_form()
# if not (str(t[0]) == str(p1) and
        # str(t[1]) == str(p2) and
        # str(t[2]) == str(Plane(normal_vector=[0,0,-2], constant_term=2)) and
        # str(t[3]) == str(Plane())):
    # print('test case 3 failed')

# p1 = Plane(normal_vector=[0,1,1], constant_term=1)
# p2 = Plane(normal_vector=[1,-1,1], constant_term=2)
# p3 = Plane(normal_vector=[1,2,-5], constant_term=3)
# s = LinearSystem([p1,p2,p3])
# t = s.compute_triangular_form()
# if not (str(t[0]) == str(Plane(normal_vector=[1,-1,1], constant_term=2)) and
        # str(t[1]) == str(Plane(normal_vector=[0,1,1], constant_term=1)) and
        # str(t[2]) == str(Plane(normal_vector=[0,0,-9], constant_term=-2))):
    # print('test case 4 failed')
