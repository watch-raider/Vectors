import math
from decimal import Decimal

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
        
    def plus(self, vector):
        result = []
        
        for x in range(self.dimension):
            result.append(float("%.3f" % (self.coordinates[x] + vector.coordinates[x])))
            
        return Vector(result)
        
    def minus(self, vector):
        result = []
        
        for x in range(self.dimension):
            result.append(float("%.3f" % (self.coordinates[x] - vector.coordinates[x])))
            
        return Vector(result)
    
    
    def multiply(self, scalar):
        result = []
        
        for x in range(self.dimension):
            result.append(float("%.3f" % (self.coordinates[x] * scalar)))
            
        return Vector(result)
       
    # refers to how much movement a vector quantifies
    def magnitude(self):
        result = []
        
        for x in range(self.dimension):
            result.append(self.coordinates[x]**2)
        
        return math.sqrt(sum(result))
        
    # refers to where a vector's movement is pointed
    # returns Normalised vector (process of finding a unit vector in the same direction as a given vector)
    def direction(self):
        magnitude_result = self.magnitude()
        normalised_unit = 1.0 / magnitude_result
            
        return self.multiply(normalised_unit)
       
    # allows us to find the angle between two vectors
    def dot_product(self, vector):
        result = []
        
        for x in range(self.dimension):
            result.append((self.coordinates[x] * vector.coordinates[x]))
            
        return sum(result)
       
    # returns the angle between two vectors
    def angle(self, vector, in_degrees=False):
        try:
            magnitude_result = self.magnitude()
            magnitude_result_1 = vector.magnitude()
            
            result = math.acos(self.dot_product(vector) / (magnitude_result * magnitude_result_1))
            
            degrees_per_radions = 180 / math.pi
            if in_degrees:
                return result * degrees_per_radions
            else:
                return result
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with 0 vector')
            else:
                raise e
    
    # Checks if vector is scalar multiple of other vector
    def is_parallel(self, vector):
        zero_vector = self.multiply(0)
        
        if vector == zero_vector:
            return True
        
        normalised_vector = self.direction()
        normalised_vector_1 = vector.direction()
        inverted_vector = normalised_vector.multiply(-1)
        
        if normalised_vector_1 == normalised_vector or normalised_vector_1 == inverted_vector:
            return True
        else:
            return False
    
    # Vectors are orthogonal is their dot product is 0
    # Note: 0 vector is orthogonal to all vectors
    def is_orthogonal(self, vector):
        dot_result = self.dot_product(vector)
        
        if dot_result == 0:
            return True
            
        angle_degrees = self.angle(vector, True)
        
        if angle_degrees == 90:
            return True    
        else:
            return False
    
    # returns projection one vector onto another
    def projection(self, vector):
        try:
            normalised_vector = vector.direction()
            magnitude = self.dot_product(normalised_vector)
            
            return normalised_vector.multiply(magnitude)
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
        
    # Component of first vector orthogonal to second vector
    def orthogonal(self, vector):
        try:
            projection_result = self.projection(vector)
            return self.minus(projection_result)
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
        
    # returns vector that is orthogonal to both vectors
    def cross_product(self, vector):
        cp_result = []
        
        x_1, y_1, z_1 = self.coordinates
        x_2, y_2, z_2 = vector.coordinates
        
        cp_result.append(float("%.3f" % (y_1*z_2 - y_2*z_1)))
        cp_result.append(float("%.3f" % -(x_1*z_2 - x_2*z_1)))
        cp_result.append(float("%.3f" % (x_1*y_2 - x_2*y_1)))
        
        return Vector(cp_result)
        
    def parallelogram_area(self, vector):
        cp_result = self.cross_product(vector)
        return cp_result.magnitude()
        
    def triangle_area(self, vector):
        cp_result = self.cross_product(vector)
        return 0.5 * cp_result.magnitude()


##################################
#print('Plus, Minus, Scalar Multiply')
#
#vector = Vector([8.218, -9.341])
#vector_1 = Vector([-1.129, 2.111])
#print(vector.plus(vector_1))
#
#vector = Vector([7.119, 8.215])
#vector_1 = Vector([-8.223, 0.878])
#print(vector.minus(vector_1))
#
#vector = Vector([1.671, -1.012, -0.318])
#scalar = 7.41
#print(vector.multiply(scalar))
#
###################################
#print('\n')
#print('Magnitude & Direction')
#
#vector = Vector([-0.221, 7.437])
#print(float("%.3f" % vector.magnitude()))
#
#vector = Vector([8.813, -1.331, -6.247])
#print(float("%.3f" % vector.magnitude()))
#
#vector = Vector([5.581, -2.136])
#print(vector.direction())
#
#vector = Vector([1.996, 3.108, -4.554])
#print(vector.direction())
#
###################################
#print('\n')
#print('Dot Product & Angle')
#
#vector = Vector([7.887, 4.138])
#vector_1 = Vector([-8.802, 6.776])
#print(float("%.3f" % vector.dot_product(vector_1)))
#
#vector = Vector([-5.955, -4.904, -1.874])
#vector_1 = Vector([-4.496, -8.755, 7.103])
#print(float("%.3f" % vector.dot_product(vector_1)))
#
#vector = Vector([3.183, -7.627])
#vector_1 = Vector([-2.668, 5.319])
#print(float("%.3f" % vector.angle(vector_1)))
#
#vector = Vector([7.35, 0.221, 5.188])
#vector_1 = Vector([2.751, 8.259, 3.985])
#print(float("%.3f" % (vector.angle(vector_1, True))))
#
#
###################################
#print('\n')
#print('Parallel & Orthogonal Vectors')
#
#vector = Vector([-7.579, -7.88])
#vector_1 = Vector([22.737, 23.64])
#print(vector.is_parallel(vector_1))
#
#vector = Vector([-2.029, 9.97, 4.172])
#vector_1 = Vector([-9.231, -6.639, -7.245])
#print(vector.is_parallel(vector_1))
#
#vector = Vector([-2.328, -7.284, -1.214])
#vector_1 = Vector([-1.821, 1.072, -2.94])
#print(vector.is_parallel(vector_1))
#
#vector = Vector([2.118, 4.827])
#vector_1 = Vector([0, 0])
#print(vector.is_parallel(vector_1))
#
#print('\n')
#
#vector = Vector([-7.579, -7.88])
#vector_1 = Vector([22.737, 23.64])
#print(vector.is_orthogonal(vector_1))
#
#vector = Vector([-2.029, 9.97, 4.172])
#vector_1 = Vector([-9.231, -6.639, -7.245])
#print(vector.is_orthogonal(vector_1))
#
#vector = Vector([-2.328, -7.284, -1.214])
#vector_1 = Vector([-1.821, 1.072, -2.94])
#print(vector.is_orthogonal(vector_1))
#
#vector = Vector([2.118, 4.827])
#vector_1 = Vector([0, 0])
#print(vector.is_orthogonal(vector_1))
#
#
###################################
#print('\n')
#print('Projecting Vectors')
#
#vector = Vector([3.039, 1.879])
#vector_1 = Vector([0.825, 2.036])
#print(vector.projection(vector_1))
#
#vector = Vector([-9.88, -3.264, -8.159])
#vector_1 = Vector([-2.155, -9.353, -9.473])
#print(vector.orthogonal(vector_1))
#
#vector = Vector([3.009, -6.172, 3.692, -2.51])
#vector_1 = Vector([6.404, -9.144, 2.759, 8.178])
#projection_result = vector.projection(vector_1)
#orthogonal_result = vector.orthogonal(vector_1)
#print(projection_result)
#print(orthogonal_result)
#
###################################
#print('\n')
#print('Cross Products')
#
#vector = Vector([8.462, 7.893, -8.187])
#vector_1 = Vector([6.984, -5.975, 4.778])
#print(vector.cross_product(vector_1))
#
#vector = Vector([-8.987, -9.838, 5.031])
#vector_1 = Vector([-4.268, -1.861, -8.866])
#print(float("%.3f" % vector.parallelogram_area(vector_1)))
#
#vector = Vector([1.5, 9.547, 3.691])
#vector_1 = Vector([-6.007, 0.124, 5.772])
#print(float("%.3f" % vector.triangle_area(vector_1)))