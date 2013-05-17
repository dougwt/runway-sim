class Customer():
    def __init__(self, id, interarrivalTime, serviceTime, prevEndTime, clock):
        self.id = id                                # order of arrival
        self.interarrivalTime = interarrivalTime    # based on random value
        self.serviceLength = serviceTime            # based on random value

        # previous arrivalTime + interarrivalTime
        self.arrivalTime = clock + self.interarrivalTime

        # max(arrival time, previous end time)
        self.serviceTimeBegins = max(self.arrivalTime, prevEndTime)

        # serviceTimeBegins - arrivalTime
        self.waitingTimeInQueue = self.serviceTimeBegins - self.arrivalTime

        # serviceTimeBegins + serviceLength
        self.serviceTimeEnds = self.serviceTimeBegins + self.serviceLength

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
                  self.serviceLength,
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
