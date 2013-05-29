#! /usr/bin/python
# customer.py
#
# Description
#
# CSS 458 - Group Project - Spring 2013
# Doug Tyler <dougwt@gmail.com>
# Elliott Shanks <shanksfamily3012@gmail.com>
# Hien Phu Luong <phuhien@uw.edu>
#
# Assumptions:
# TODO: Assumptions

class Customer():
    def __init__(self, id, interarrivalTime, serviceTime1, serviceTime2,
            balk, prevCust, clock):
        """Initializes customer data based on initial data."""
        self.id = id                                # order of arrival
        self.interarrivalTime = interarrivalTime
        self.serviceTime1 = serviceTime1
        self.serviceTime2 = serviceTime2
        self.balk = balk

        # initialize values from previous customer
        if prevCust:
            prevServiceTime1Begins = prevCust.serviceTime1Begins
            prevServiceTime1Ends = prevCust.serviceTime1Ends
            prevServiceTime2Begins = prevCust.serviceTime2Begins
            prevServiceTime2Ends = prevCust.serviceTime2Ends
        else:
            prevServiceTime1Begins = 0
            prevServiceTime1Ends = 0
            prevServiceTime2Begins = 0
            prevServiceTime2Ends = 0

        # process Q1/S1
        self.arrivalTime1 = clock + self.interarrivalTime
        self.serviceTime1Begins = max(self.arrivalTime1, prevServiceTime1Ends)
        self.serviceTime1Ends = self.serviceTime1Begins + self.serviceTime1
        self.waitTime1 = self.serviceTime1Begins - self.arrivalTime1

        # process Q2/S2
        if self.balk is False:
            self.arrivalTime2 = self.serviceTime1Ends
            self.serviceTime2Begins = max(self.arrivalTime2, prevServiceTime2Ends)
            self.serviceTime2Ends = self.serviceTime2Begins + self.serviceTime2
            self.waitTime2 = self.serviceTime2Begins - self.arrivalTime2
            self.totalWait = self.waitTime1 + self.waitTime2
            self.timeInSystem = self.serviceTime2Ends - self.arrivalTime1
            self.idleTime = (self.serviceTime1Begins - prevServiceTime1Ends) \
                + (self.serviceTime2Begins - prevServiceTime2Ends)
        else:
            self.arrivalTime2 = self.serviceTime1Ends
            self.serviceTime2Begins = prevServiceTime2Begins
            self.serviceTime2Ends = prevServiceTime2Ends
            self.waitTime2 = 0
            self.totalWait = self.waitTime1 + self.waitTime2
            self.timeInSystem = self.serviceTime1Ends - self.arrivalTime1
            self.idleTime = (self.serviceTime1Begins - prevServiceTime1Ends)

    def __str__(self):
        """Used to generate a columned printout of customers."""
        values = (self.id,
                  # ('%.2f -> %d' % (self.probInterarrival, self.interarrivalTime))[1:],
                  # ('%.2f -> %d' % (self.probService1, self.serviceTime1))[1:],
                  # ('%.2f -> %d' % (self.probService2, self.serviceTime2))[1:],
                  # ('%.2f -> %s' % (self.probBalk, 'Y' if self.balk else '-'))[1:],
                  self.interarrivalTime,
                  self.serviceTime1,
                  self.serviceTime2,
                  # 'Y' if self.balk else '-',
                  self.arrivalTime1,
                  self.waitTime1,
                  self.serviceTime1Begins,
                  self.serviceTime1Ends,
                  self.waitTime2 if not self.balk else '-',
                  self.serviceTime2Begins if not self.balk else '--',
                  self.serviceTime2Ends if not self.balk else '--',
                  self.totalWait,
                  self.timeInSystem)

        values = [str(i).center(10) for i in values]

        output = ''
        for value in values:
            output += str(value)

        return output

    # def calcInterarrivalTime(self, probInterarrival):
    #     """Maps a probability distribution to interrarrival times."""
    #     if probInterarrival < 0.2:
    #         return 0
    #     elif probInterarrival >= 0.2 and probInterarrival <= 0.6:
    #         return 1
    #     else:
    #         return 2

    # def calcServiceTime1(self, probService1):
    #     """Maps a probability distribution to serviceTime1."""
    #     if probService1 < 0.2:
    #         return 1
    #     elif probService1 >= 0.2 and probService1 <= 0.6:
    #         return 2
    #     else:
    #         return 3

    # def calcServiceTime2(self, probService2):
    #     """Maps a probability distribution to serviceTime2."""
    #     if probService2 < 0.2:
    #         return 1
    #     elif probService2 >= 0.2 and probService2 <= 0.6:
    #         return 2
    #     else:
    #         return 3

    # def calcBalk(self, probBalk):
    #     """Maps a probability distribution to balk decision."""
    #     return probBalk <= 0.33
