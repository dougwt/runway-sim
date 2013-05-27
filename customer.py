class Customer():
    def __init__(self, id, probInterarrival, probService1, probService2, probBalk, prevEndTime, clock):
        """Initializes customer data based on initial data."""
        self.id = id                                # order of arrival

        # generate random values based on probability distributions
        self.interarrivalTime = self.calcInterarrivalTime(probInterarrival)
        self.serviceTime1 = self.calcServiceTime1(probService1)
        self.serviceTime2 = self.calcServiceTime2(probService2)
        self.balk = self.calcBalk(probBalk)

        # previous arrivalTime + interarrivalTime
        self.arrivalTime = clock + self.interarrivalTime

        # max(arrival time, previous end time)
        self.serviceTime1Begins = max(self.arrivalTime, prevEndTime)
        self.serviceTime2Begins = 0

        # serviceTimeBegins - arrivalTime
        self.waitingTimeInQueue = self.serviceTime1Begins - self.arrivalTime

        # serviceTimeBegins + serviceTime
        self.serviceTime1Ends = self.serviceTime1Begins + self.serviceTime1
        self.serviceTime2Ends = 0

        # serviceTimeEnds - arrivalTime
        self.timeInSystem = self.serviceTime1Ends - self.arrivalTime

        # serviceTimeBegins - previous end time
        self.idleTime = self.serviceTime1Begins - prevEndTime

        # increments current clock time
        # clock += interarrivalTime

    def __str__(self):
        """Used to generate a columned printout of customers."""
        values = (self.id,
                  self.interarrivalTime,
                  self.arrivalTime,
                  self.serviceTime1,
                  self.serviceTime2,
                  self.balk,
                  self.serviceTime1Begins,
                  self.serviceTime1Ends,
                  self.serviceTime2Begins,
                  self.serviceTime2Ends,
                  self.waitingTimeInQueue,
                  self.timeInSystem)
                  # self.idleTime)

        values = [str(i).center(10) for i in values]

        output = ''
        for value in values:
            output += str(value)

        return output

    def calcInterarrivalTime(self, probInterarrival):
        """Maps a probability distribution to interrarrival times."""
        if probInterarrival < 0.2:
            return 1
        elif probInterarrival >= 0.2 and probInterarrival <= 0.6:
            return 2
        else:
            return 3

    def calcServiceTime1(self, probService1):
        """Maps a probability distribution to serviceTime1."""
        if probService1 < 0.2:
            return 1
        elif probService1 >= 0.2 and probService1 <= 0.6:
            return 2
        else:
            return 3

    def calcServiceTime2(self, probService2):
        """Maps a probability distribution to serviceTime2."""
        if probService2 < 0.2:
            return 1
        elif probService2 >= 0.2 and probService2 <= 0.6:
            return 2
        else:
            return 3

    def calcBalk(self, probBalk):
        """Maps a probability distribution to balk decision."""
        return probBalk <= 0.5


def counter():
    """A generator that counts upwards from 1."""
    id = 1;
    while True:
        yield id
        id += 1

def main():
    import random
    id = counter()
    num = 10
    random.seed(1234)
    for i in xrange(10):
        probInterarrival = random.random()
        probService1 = random.random()
        probService2 = random.random()
        probBalk = random.random()
        print Customer(id.next(), probInterarrival, probService1, probService2, probBalk, 10, 20)

if __name__ == '__main__':
    main()
