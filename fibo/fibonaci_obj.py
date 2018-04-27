class Fibonaci(object):
    def __init__(self, num):
        self.a = 0
        self.b = 1
        self.cur = 0
        self.num = num

    def __iter__(self):
        return self 

    def __next__(self):
        if self.cur < self.num:
            ret = self.a
            self.a, self.b = self.b, self.a+self.b
            self.cur += 1
            return ret
        else:
            raise StopIteration


if __name__ == '__main__':
    fibo = Fibonaci(10)
    for num in fibo:
        print(num)
