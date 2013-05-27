import random
from customer import Customer


class Simulation():
    def __init__(self, numCustomers=100):
        """Initializes the simulation."""
        self.numCustomers = numCustomers
        self.clock = 0
        self.queue = []

        # additional values to be calculated during simulation
        self.averageWaitingTime = 0         # average waiting time for all customers
        self.averageWaitingTimeWhoWait = 0  # avg waiting time for customers who wait
        self.averageServiceTime = 0         # average service time for all customers
        self.averageInterarrrivalTime = 0   # average interarrival time for all customers
        self.averageSystemTime = 0          # average total system time for all customers
        self.waitProbability = 0            # probability a customer has to wait
        self.idleProbability = 0            # percentage of time server is idle

        self.populate()

    def populate(self):
        """Populates Q1 with the pool of Customers."""
        for i in range(self.numCustomers):
            probInterarrival, probService1, probService2, probBalk = self.generateRandomValues()

            if (i == 0):
                prevEndTime = 0
            else:
                prevEndTime = self.queue[i-1].serviceTime1Ends

            # customer = Customer(i+1, interarrivalTime, serviceTime, prevEndTime, self.clock)
            customer = Customer(i+1, probInterarrival, probService1, probService2, probBalk, prevEndTime, self.clock)
            self.queue.append(customer)
            self.clock = customer.arrivalTime
        self.calculateStats()

    def generateRandomValues(self):
        """Generates random value for Customer creation."""
        # probInterarrival = self.determineServiceTime(random.randrange(1, 101))
        probInterarrival = random.random()
        probService1 = random.random()
        probService2 = random.random()
        probBalk = random.random()
        return (probInterarrival, probService1, probService2, probBalk)

    def determineServiceTime(self, interarrivalRandom):
        """Determines service time based on interarrivalRandom."""
        if(interarrivalRandom <= 10):
            return 1
        elif(interarrivalRandom >= 11 and interarrivalRandom <= 30):
            return 2
        elif(interarrivalRandom >= 31 and interarrivalRandom <= 60):
            return 3
        elif(interarrivalRandom >= 61 and interarrivalRandom <= 85):
            return 4
        elif(interarrivalRandom >= 86 and interarrivalRandom <= 95):
            return 5
        else:  # 96 - 100
            return 6

    def calculateStats(self):
        """Calculates total and average stats."""
        # temporary variables used for calculating averages/etc
        totalWaitingTime = 0
        totalServiceTime = 0
        totalSystemTime = 0
        totalIdleTime = 0
        totalIterarrivalTime = 0
        totalSimulationTime = self.queue[-1].serviceTime1Ends
        numCustomersWhoWait = 0

        # iterate through each customer in the queue
        for customer in self.queue:
            totalWaitingTime += customer.waitingTimeInQueue
            totalIdleTime += customer.idleTime
            totalServiceTime += customer.serviceTime1
            totalIterarrivalTime += customer.interarrivalTime
            totalSystemTime += customer.timeInSystem

            if customer.waitingTimeInQueue > 0:
                numCustomersWhoWait += 1

        # calculate the averages/etc
        self.averageWaitingTime = totalWaitingTime / self.numCustomers
        if numCustomersWhoWait > 0:
            self.averageWaitingTimeWhoWait = totalWaitingTime / numCustomersWhoWait
        self.averageServiceTime = totalServiceTime / self.numCustomers
        self.averageInterarrrivalTime = totalIterarrivalTime / (self.numCustomers - 1)
        self.averageSystemTime = totalSystemTime / self.numCustomers
        self.waitProbability = numCustomersWhoWait / self.numCustomers
        self.idleProbability = totalIdleTime / totalSimulationTime

    def display(self):
        """Displays an event log of activity."""
        headers = (('Customer', '#'),
                   ('InterArr', 'Time'),
                   ('Arrival', 'Time'),
                   ('S1', 'Time'),
                   ('S2', 'Time'),
                   ('Balk', 'Decision'),
                   ('S1 Start', 'Time'),
                   ('S1 End', 'Time'),
                   ('S2 Start', 'Time'),
                   ('S2 End', 'Time'),
                   ('Waiting', 'Time'),
                   ('System', 'Time'),
                   ('S1', 'Idle'),
                   ('S2', 'Idle'))
                   # ('Idle', 'Time'))

        headers1, headers2 = zip(*headers)

        field_width = 10  # number of characters per field_width
        columns = len(headers)

        # horizontal line
        print '-' * field_width * columns

        headers = [i.center(field_width) for i in headers1]
        print ''.join(headers)

        # 2nd line of header column
        headers = [i.center(field_width) for i in headers2]
        print ''.join(headers)

        # horizontal line
        print '-' * field_width * columns

        # print row for each customer
        for customer in self.queue:
            s1idle = False
            s2idle = True
            print '%s%s%s' % (customer, str(s1idle).center(field_width), str(s2idle).center(field_width))

        print
        print "%60s:  %5.2f  minutes" % ("Average waiting time for all customers", self.averageWaitingTime)
        print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", self.averageWaitingTimeWhoWait)
        print "%60s:  %5.2f  minutes" % ("Average service time", self.averageServiceTime)
        print "%60s:  %5.2f  minutes" % ("Average time between arrivals", self.averageInterarrrivalTime)
        print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", self.averageSystemTime)
        print "%60s:  %5d  %%" % ("Probability a customer has to wait in the queue", self.waitProbability * 100)
        print "%60s:  %5d  %%" % ("Percentage of time server is idle", self.idleProbability * 100)


# def runTrials(numTrials=10, numCustomers=10, verbose=True):
#     averageWaitingTime = 0
#     averageWaitingTimeWhoWait = 0
#     averageServiceTime = 0
#     averageInterarrrivalTime = 0
#     averageSystemTime = 0
#     waitProbability = 0
#     idleProbability = 0
#     trials = []

#     for i in range(numTrials):
#         trial = Simulation(numCustomers)

#         if (verbose):
#             print
#             print "Trial %d" % (i + 1)
#             trial.display()

#         trials.append(trial)

#         averageWaitingTime += trial.averageWaitingTime
#         averageWaitingTimeWhoWait += trial.averageWaitingTimeWhoWait
#         averageServiceTime += trial.averageServiceTime
#         averageInterarrrivalTime += trial.averageInterarrrivalTime
#         averageSystemTime += trial.averageSystemTime
#         waitProbability += trial.waitProbability
#         idleProbability += trial.idleProbability

#     averageWaitingTime /= numTrials
#     averageWaitingTimeWhoWait /= numTrials
#     averageServiceTime /= numTrials
#     averageInterarrrivalTime /= numTrials
#     averageSystemTime /= numTrials
#     waitProbability /= numTrials
#     idleProbability /= numTrials

#     print
#     print '-'*79
#     print "Averages for %d Completed Trials (%d Customers per Trial):" % (numTrials, numCustomers)
#     print '-'*79
#     print "%60s:  %5.2f  minutes" % ("Average waiting time for all customers", averageWaitingTime)
#     print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", averageWaitingTimeWhoWait)
#     print "%60s:  %5.2f  minutes" % ("Average service time", averageServiceTime)
#     print "%60s:  %5.2f  minutes" % ("Average time between arrivals", averageInterarrrivalTime)
#     print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", averageSystemTime)
#     print "%60s:  %5d  %%" % ("Probability a customer has to wait in the queue", waitProbability * 100)
#     print "%60s:  %5d  %%" % ("Percentage of time server is idle", idleProbability * 100)


def main():
    # numTrials = 10
    # numCustomersPerTrial = 10
    # displayStats = True

    # # run multiple trials and display averages
    # runTrials(numTrials, numCustomersPerTrial, displayStats)

    numCustomers = 10
    sim = Simulation(numCustomers)
    sim.display()

    # id = Customer.counter()
    # num = 10
    # random.seed(1234)
    # for i in xrange(10):
    #     probInterarrivalTime = random.random()
    #     probServiceTime1 = random.random()
    #     probServiceTime2 = random.random()
    #     probBalk = random.random()
    #     print Customer(id.next(), probInterarrivalTime, probServiceTime1, probServiceTime2, probBalk, 10, 20)

if __name__ == '__main__':
    main()
