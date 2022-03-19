class Test(object):
    def __init__(self, x):
        self.x = x

    @property
    def x(self):
        return self.__X

    @x.setter
    def x(self, x):
        self.__X = x


t = Test('ar')

print(t.x)
t.x = 12
print(t.x)
