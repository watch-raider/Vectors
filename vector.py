import math

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
        
    def magnitude(self):
        result = []
        
        for x in range(self.dimension):
            result.append(self.coordinates[x]**2)
        
        return math.sqrt(sum(result))
        
    def direction(self):
        magnitude_result = self.magnitude()
    
        result = []
        normalised_unit = 1 / magnitude_result
            
        return self.multiply(normalised_unit)
        
    def dot_product(self, vector):
        result = []
        
        for x in range(self.dimension):
            result.append((self.coordinates[x] * vector.coordinates[x]))
            
        return sum(result)
        
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


##################################
print('Plus, Minus, Scalar Multiply')
vector = Vector([8.218, -9.341])
vector_1 = Vector([-1.129, 2.111])
print(vector.plus(vector_1))

vector = Vector([7.119, 8.215])
vector_1 = Vector([-8.223, 0.878])
print(vector.minus(vector_1))

vector = Vector([1.671, -1.012, -0.318])
scalar = 7.41
print(vector.multiply(scalar))

##################################
print('\n')
print('Magnitude & Direction')
vector = Vector([-0.221, 7.437])
print(float("%.3f" % vector.magnitude()))

vector = Vector([8.813, -1.331, -6.247])
print(float("%.3f" % vector.magnitude()))

vector = Vector([5.581, -2.136])
print(vector.direction())

vector = Vector([1.996, 3.108, -4.554])
print(vector.direction())

##################################
print('\n')
print('Dot Product & Angle')
vector = Vector([7.887, 4.138])
vector_1 = Vector([-8.802, 6.776])
print(float("%.3f" % vector.dot_product(vector_1)))

vector = Vector([-5.955, -4.904, -1.874])
vector_1 = Vector([-4.496, -8.755, 7.103])
print(float("%.3f" % vector.dot_product(vector_1)))

vector = Vector([3.183, -7.627])
vector_1 = Vector([-2.668, 5.319])
print(float("%.3f" % vector.angle(vector_1)))

vector = Vector([7.35, 0.221, 5.188])
vector_1 = Vector([2.751, 8.259, 3.985])
print(float("%.3f" % (vector.angle(vector_1, True))))