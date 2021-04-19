
class Rectangle:

    def __init__(self, triangle2D):
        self.min_y, self.max_y = triangle2D.get_min_max_y()
        self.min_x, self.max_x = triangle2D.get_min_max_x()

    def does_overlap(self, other):
        
        x_overlap = False
        y_overlap = False

        # check x axis
        if self.max_x > other.min_x and other.min_x >= self.min_x:
            x_overlap = True
        elif other.max_x > self.min_x and self.min_x >= other.min_x:
            x_overlap = True

        # check y axis
        if self.max_y > other.min_y and other.min_y >= self.min_y:
            y_overlap = True
        elif other.max_y > self.min_y and self.min_y >= other.min_y:
            y_overlap = True

        return x_overlap and y_overlap