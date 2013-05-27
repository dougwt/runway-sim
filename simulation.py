import random
from customer import Customer


class Simulation():
    def __init__(self, numCustomers=100):
        """Initializes the simulation."""
        self.numCustomers = numCustomers
        self.queue = []

        # initialize State Variables
        self.clock = 0
        self.Idle = 0
        self.Busy = 1
        self.s1 = self.Idle
        self.s2 = self.Idle
        self.q1 = 0
        self.q2 = 0

        # additional values to be calculated during simulation
        self.averageWaitingTime = 0         # average waiting time for all customers
        self.averageWaitingTimeWhoWait = 0  # avg waiting time for customers who wait
        self.averageServiceTime = 0         # average service time for all customers
        self.averageInterarrrivalTime = 0   # average interarrival time for all customers
        self.averageSystemTime = 0          # average total system time for all customers
        self.waitProbability = 0            # probability a customer has to wait
        self.idleProbability = 0            # percentage of time server is idle
        self.averageQ1Time = 0
        self.averageQ2Time = 0
        self.q1sizes = {}
        self.q2sizes = {}

        self.populate()

    def populate(self):
        """Populates Q1 with the pool of Customers."""
        for i in range(self.numCustomers):
            self.generateCustomer(i)

        self.calculateStats()
        # print 'Q1:', self.q1sizes
        # print 'Q2:', self.q2sizes

    def generateCustomer(self, i):
        """Generates a new customer and processes it through Q1 and Q2."""
        # generate and unpack random values used for the new customer
        probInterarrival, probService1, probService2, probBalk = self.generateRandomValues()

        # if this is the first iteration, there is no previous customer
        if (i == 0):
            prevCust = None
        else:
            prevCust = self.queue[i-1]

        # generate a new Customer and store it into the system queue
        id = i + 1
        customer = Customer(id, probInterarrival, probService1, probService2, probBalk, prevCust, self.clock)
        self.queue.append(customer)

        # update clock to the time the customer first arrives in the system
        self.clock = customer.arrivalTime1

        # determine sizes of q1 and q2 at time of arrivals
        self.q1 = len([x for x in self.queue[:-1] if x.serviceTime1Ends > customer.arrivalTime1])
        self.q2 = len([x for x in self.queue[:-1] if x.balk is False and x.serviceTime2Ends > customer.arrivalTime2])

        # store queue sizes for later display
        self.q1sizes[id] = self.q1
        self.q2sizes[id] = self.q2

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
        lastCust = self.queue[-1]
        totalSimulationTime = lastCust.serviceTime2Ends if not lastCust.balk else lastCust.serviceTime1Ends
        numCustomersWhoWait = 0
        totalQ1WaitTime = 0
        totalQ2WaitTime = 0
        numCustomersQ1 = 0
        numCustomersQ2 = 0

        # iterate through each customer in the queue
        for customer in self.queue:
            totalWaitingTime += customer.totalWait
            # totalIdleTime += customer.idleTime
            totalServiceTime += customer.serviceTime1 + customer.serviceTime2
            totalIterarrivalTime += customer.interarrivalTime
            totalSystemTime += customer.timeInSystem

            if customer.totalWait > 0:
                numCustomersWhoWait += 1

            if customer.waitTime1 > 0:
                numCustomersQ1 += 1

            totalQ1WaitTime += customer.waitTime1
            if customer.balk is False:
                totalQ2WaitTime += customer.waitTime2
                if customer.waitTime2 > 0:
                    numCustomersQ2 += 1

        # calculate the averages/etc
        self.averageQ1Time = totalQ1WaitTime / float(self.numCustomers)
        self.averageQ2Time = totalQ2WaitTime / float(numCustomersWhoWait)

        self.averageWaitingTime = totalWaitingTime / float(self.numCustomers)
        if numCustomersWhoWait > 0:
            self.averageWaitingTimeWhoWait = totalWaitingTime / float(numCustomersWhoWait)
        self.averageServiceTime = totalServiceTime / float(self.numCustomers)
        self.averageInterarrrivalTime = totalIterarrivalTime / float(self.numCustomers - 1)
        self.averageSystemTime = totalSystemTime / float(self.numCustomers)
        self.waitProbability = numCustomersWhoWait / float(self.numCustomers)
        self.wait1Probability = numCustomersQ1 / float(self.numCustomers)
        self.wait2Probability = numCustomersQ2 / float(self.numCustomers)
        # self.idleProbability = totalIdleTime / float(totalSimulationTime)

    def display(self):
        """Displays an event log of activity."""
        headers = (('Customer', '#'),
                   ('Inter', 'Arrival'),
                   ('S1', 'Time'),
                   ('S2', 'Time'),
                   ('Balk', 'Decision'),
                   ('Arrival', 'Time'),
                   ('Q1', 'Wait'),
                   ('S1 Start', 'Time'),
                   ('S1 End', 'Time'),
                   ('Q2', 'Wait'),
                   ('S2 Start', 'Time'),
                   ('S2 End', 'Time'),
                   ('Total', 'Wait'),
                   ('Total', 'System'),
                   ('Q1', 'Size'),
                   ('Q2', 'Size'))
                   # ('S1', 'Idle'),
                   # ('S2', 'Idle'))
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
            q1size = self.q1sizes[customer.id]
            q2size = self.q2sizes[customer.id]
            print '%s%s%s' % (customer, str(q1size).center(field_width), str(q2size).center(field_width))

        print
        print "%60s:  %5.2f  minutes" % ("Average Q1 wait time", self.averageQ1Time)
        print "%60s:  %5.2f  minutes" % ("Average Q2 wait time", self.averageQ2Time)
        print
        print "%60s:  %5.2f  minutes" % ("Average total waiting time for all customers", self.averageWaitingTime)
        print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", self.averageWaitingTimeWhoWait)
        print "%60s:  %5.2f  minutes" % ("Average total service time", self.averageServiceTime)
        print "%60s:  %5.2f  minutes" % ("Average time between arrivals", self.averageInterarrrivalTime)
        print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", self.averageSystemTime)
        print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q1", self.wait1Probability * 100)
        print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q2", self.wait2Probability * 100)
        # print "%60s:  %5d  %%" % ("Percentage of time server is idle", self.idleProbability * 100)


def runTrials(numTrials=10, numCustomers=10, verbose=True):
    averageQ1Time = 0
    averageQ2Time = 0
    averageWaitingTime = 0
    averageWaitingTimeWhoWait = 0
    averageServiceTime = 0
    averageInterarrrivalTime = 0
    averageSystemTime = 0
    waitProbability = 0
    wait1Probability = 0
    wait2Probability = 0
    idleProbability = 0
    trials = []

    for i in range(numTrials):
        trial = Simulation(numCustomers)

        if (verbose):
            print
            print "Trial %d" % (i + 1)
            trial.display()

        trials.append(trial)

        averageQ1Time += trial.averageQ1Time
        averageQ2Time += trial.averageQ2Time
        averageWaitingTime += trial.averageWaitingTime
        averageWaitingTimeWhoWait += trial.averageWaitingTimeWhoWait
        averageServiceTime += trial.averageServiceTime
        averageInterarrrivalTime += trial.averageInterarrrivalTime
        averageSystemTime += trial.averageSystemTime
        waitProbability += trial.waitProbability
        wait1Probability += trial.wait1Probability
        wait2Probability += trial.wait2Probability
        idleProbability += trial.idleProbability

    numTrials = float(numTrials)
    averageQ1Time /= numTrials
    averageWaitingTime /= numTrials
    averageWaitingTime /= numTrials
    averageWaitingTimeWhoWait /= numTrials
    averageServiceTime /= numTrials
    averageInterarrrivalTime /= numTrials
    averageSystemTime /= numTrials
    waitProbability /= numTrials
    wait1Probability /= numTrials
    wait2Probability /= numTrials
    idleProbability /= numTrials

    print
    print '-'*79
    print "Averages for %d Completed Trials (%d Customers per Trial):" % (numTrials, numCustomers)
    print '-'*79
    print "%60s:  %5.2f  minutes" % ("Average Q1 wait time", averageQ1Time)
    print "%60s:  %5.2f  minutes" % ("Average Q2 wait time", averageQ2Time)
    print
    print "%60s:  %5.2f  minutes" % ("Average total waiting time for all customers", averageWaitingTime)
    print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", averageWaitingTimeWhoWait)
    print "%60s:  %5.2f  minutes" % ("Average total service time", averageServiceTime)
    print "%60s:  %5.2f  minutes" % ("Average time between arrivals", averageInterarrrivalTime)
    print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", averageSystemTime)
    print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q1", wait1Probability * 100)
    print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q2", wait2Probability * 100)
    # print "%60s:  %5d  %%" % ("Percentage of time server is idle", idleProbability * 100)


def main():
    numTrials = 3
    numCustomersPerTrial = 10
    displayStats = True

    # run multiple trials and display averages
    runTrials(numTrials, numCustomersPerTrial, displayStats)

    # numCustomers = 10
    # sim = Simulation(numCustomers)
    # sim.display()

if __name__ == '__main__':
    main()
