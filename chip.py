'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''


class Chip:

    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
        self.x_pos = None
        self.y_pos = None
        self.SPEED = 0
        if color == "RED":
            self.rgb = (1, 0, 0)
        elif color == "YELLOW":
            self.rgb = (1, 1, 0)

    def display(self, x=None, y=None):
        '''
        Method to display the chip

        It takes 2 optional arguments. if the arguments are not
        specified, will output the x_pos and y_pos attributes
        '''
        fill(*self.rgb)
        if x and y:
            circle(x, y, self.radius)
        else:
            circle(self.x_pos, self.y_pos, self.radius)

    def display_fall(self, acc=10):
        '''
        Same display method with y position updates
        '''
        self.SPEED += acc
        self.y_pos += self.SPEED
        self.display()
