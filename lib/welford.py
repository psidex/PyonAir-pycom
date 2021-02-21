class WelfordAverage:
    # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    # Do the average in a single pass!

    def __init__(self, logger=None, count=0, mean=0, m2=0):
        self.logger = logger
        self.count = count
        self.mean = mean
        self.m2 = m2

    def update(self, new_value):
        self.count += 1
        delta = new_value - self.mean
        self.mean += delta / self.count
        delta2 = new_value - self.mean
        self.m2 += delta * delta2

    def averages(self):
        """
        Get the value count, mean, and variance from an aggregate
        :return: tuple containing the given values
        :rtype: tuple
        """
        if self.count < 2:
            return (self.count, float("nan"), float("nan"))
        variance = self.m2 / (self.count - 1)
        return (self.count, self.mean, variance)


# test = WelfordAverage(logger=None)
# for i in range(1,10):
#    test.update(i)
# print(test.averages())
