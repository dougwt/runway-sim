class Customer():
    def __init__(self, id, probInterarrivalTime, probServiceTime1, probServiceTime2, probBalk, prevEndTime, clock):
        self.id = id                                # order of arrival

        # generate random values based on probability distributions
        self.interarrivalTime = self.calcInterarrivalTime(probInterarrivalTime)
        self.serviceTime1 = self.calcServiceTime1(probServiceTime1)
        self.serviceTime2 = self.calcServiceTime2(probServiceTime2)
        self.balk = self.calcBalk(probBalk)

        # previous arrivalTime + interarrivalTime
        self.arrivalTime = clock + self.interarrivalTime

        # max(arrival time, previous end time)
        self.serviceTimeBegins = max(self.arrivalTime, prevEndTime)

        # serviceTimeBegins - arrivalTime
        self.waitingTimeInQueue = self.serviceTimeBegins - self.arrivalTime

        # serviceTimeBegins + serviceTime
        self.serviceTimeEnds = self.serviceTimeBegins + self.serviceTime1

        # serviceTimeEnds - arrivalTime
        self.timeInSystem = self.serviceTimeEnds - self.arrivalTime

        # serviceTimeBegins - previous end time
        self.idleTime = self.serviceTimeBegins - prevEndTime

        # increments current clock time
        # clock += interarrivalTime

    def __str__(self):
        values = (self.id,
                  self.interarrivalTime,
                  self.arrivalTime,
                  self.serviceTime1,
                  self.serviceTime2,
                  self.balk,
                  self.serviceTimeBegins,
                  self.waitingTimeInQueue,
                  self.serviceTimeEnds,
                  self.timeInSystem,
                  self.idleTime)

        values = [str(i).center(10) for i in values]

        output = ''
        for value in values:
            output += str(value)

        return output

    def calcInterarrivalTime(self, probInterarrivalTime):
        return 1
        pass

    def calcServiceTime1(self, probServiceTime1):
        return 1
        pass

    def calcServiceTime2(self, probServiceTime2):
        return 1
        pass

    def calcBalk(self, probBalk):
        return False
        pass


def counter():
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
        probInterarrivalTime = random.random()
        probServiceTime1 = random.random()
        probServiceTime2 = random.random()
        probBalk = random.random()
        print Customer(id.next(), probInterarrivalTime, probServiceTime1, probServiceTime2, probBalk, 10, 20)

if __name__ == '__main__':
    main()
