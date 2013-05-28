from __future__ import division
import random
from customer import Customer

class Simulation():
    def __init__(self, numCustomers=100):
        """Initializes the simulation."""
        self.numCustomers = numCustomers
        self.customers = []

        # initialize State Variables
        self.clock = 0
        self.Idle = 0
        self.Busy = 1
        self.s1 = self.Idle
        self.s2 = self.Idle
        self.q1 = 0
        self.q2 = 0

        ### additional values to be tracked during simulation

        # average waiting time for all customers
        self.averageWaitingTime = 0
        self.averageQ1Time = 0
        self.averageQ2Time = 0

        # avg waiting time for customers who wait
        self.averageWaitTimeWhoWait = 0
        self.averageQ1TimeWait = 0
        self.averageQ2TimeWait = 0

        # average service time for all customers
        self.averageServiceTime = 0
        self.averageService1Time = 0
        self.averageService2Time = 0

        # avg interarrival time for all customers
        self.averageInterarrrivalTime = 0

        # avg total system time for all customers
        self.averageSystemTime = 0

        # probability a customer has to wait
        self.waitProbability = 0

        # percentage of time server is idle
        self.idleProbability = 0

        # queue sizes at the moment each customer arrived
        self.q1sizes = {}
        self.q2sizes = {}

        self.populate() # Ready. Set. Go!

    def populate(self):
        """Populates Q1 with the pool of Customers."""
        for i in range(self.numCustomers):
            self.generateCustomer(i)

        self.calculateStats()

    def generateCustomer(self, i):
        """Generates a new customer and processes it through Q1 and Q2."""
        # generate and unpack random values used for the new customer
        probInterarrival, probService1, probService2, probBalk = \
            self.generateRandomValues()

        # if this is the first iteration, there is no previous customer
        if (i == 0):
            prevCust = None
        else:
            prevCust = self.customers[i-1]

        # generate a new Customer and store it in customers
        id = i + 1
        customer = Customer(id,
                            probInterarrival,
                            probService1,
                            probService2,
                            probBalk,
                            prevCust,
                            self.clock)
        self.customers.append(customer)

        # update clock to the time the customer first arrives in the system
        self.clock = customer.arrivalTime1

        # determine sizes of q1 and q2 at time of arrivals
        self.q1 = len([x for x in self.customers[:-1] \
            if x.serviceTime1Ends > customer.arrivalTime1])
        self.q2 = len([x for x in self.customers[:-1] \
            if x.balk is False and x.serviceTime2Ends > customer.arrivalTime2])

        # store queue sizes for later display
        self.q1sizes[id] = self.q1
        self.q2sizes[id] = self.q2

    def generateRandomValues(self):
        """Generates random value for Customer creation."""

        probInterarrival = random.random()
        probService1 = random.random()
        probService2 = random.random()
        probBalk = random.random()

        return (probInterarrival, probService1, probService2, probBalk)

    def calculateStats(self):
        """Calculates total and average stats."""

        # temporary variables used for calculating averages/etc
        totalWaitingTime = 0
        totalQ1WaitTime = 0
        totalQ2WaitTime = 0

        totalServiceTime = 0
        totalService1Time = 0
        totalService2Time = 0

        totalSystemTime = 0
        totalIdleTime = 0
        totalIterarrivalTime = 0
        lastCust = self.customers[-1]
        totalSimulationTime = lastCust.serviceTime2Ends \
            if not lastCust.balk else lastCust.serviceTime1Ends
        numCustomersWhoWait = 0
        numCustomersQ1 = 0
        numCustomersQ2 = 0

        # sum up values from each customer
        for c in self.customers:
            totalWaitingTime += c.totalWait
            totalService1Time += c.serviceTime1
            if c.balk is False:
                totalService2Time += c.serviceTime2
                totalServiceTime += c.serviceTime1 + c.serviceTime2
            else:
                totalServiceTime += c.serviceTime1
            totalIterarrivalTime += c.interarrivalTime
            totalSystemTime += c.timeInSystem

            if c.totalWait > 0:
                numCustomersWhoWait += 1

            if c.waitTime1 > 0:
                numCustomersQ1 += 1

            totalQ1WaitTime += c.waitTime1
            if c.balk is False:
                totalQ2WaitTime += c.waitTime2
                if c.waitTime2 > 0:
                    numCustomersQ2 += 1

        # calculate the averages/etc
        self.averageQ1Time = totalQ1WaitTime / self.numCustomers
        self.averageQ2Time = totalQ2WaitTime / numCustomersWhoWait

        self.averageWaitingTime = totalWaitingTime / self.numCustomers
        if numCustomersWhoWait > 0:
            self.averageWaitTimeWhoWait = totalWaitingTime / numCustomersWhoWait
        if numCustomersQ1 > 0:
            self.averageQ1TimeWait = totalQ1WaitTime / numCustomersQ1
            self.averageService1Time = totalService1Time / self.numCustomers
        if numCustomersQ2 > 0:
            self.averageQ2TimeWait = totalQ2WaitTime / numCustomersQ2
            self.averageService2Time = totalService2Time / self.numCustomers
        self.averageServiceTime = totalServiceTime / self.numCustomers
        self.averageInterarrrivalTime = totalIterarrivalTime / (self.numCustomers - 1)
        self.averageSystemTime = totalSystemTime / self.numCustomers
        self.waitProbability = numCustomersWhoWait / self.numCustomers
        self.wait1Probability = numCustomersQ1 / self.numCustomers
        self.wait2Probability = numCustomersQ2 / self.numCustomers

    def display(self):
        """Displays an event log of activity."""
        headers = (('Customer', '#'),
                   ('Inter', 'Arrival'),
                   ('S1', 'Time'),
                   ('S2', 'Time'),
                   ('', 'Balk?'),
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

        # use python magic to unzip the nested tuples
        headers1, headers2 = zip(*headers)

        field_width = 10         # number of characters per field_width
        columns = len(headers)   # number of columns

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
        for customer in self.customers:
            q1size = self.q1sizes[customer.id]
            q2size = self.q2sizes[customer.id]

            q1size = q1size if q1size > 0 else '-'
            q2size = q2size if q2size > 0 else '-'

            print '%s%s%s' % (customer,
                              str(q1size).center(field_width),
                              str(q2size).center(field_width))
        print

        h = "%60s:  %5.2f  minutes     [ Q1:%5.2f minutes   Q2:%5.2f minutes ]"
        print h % ("Average waiting time for all customers",
                   self.averageWaitingTime,
                   self.averageQ1Time,
                   self.averageQ2Time)
        print h % ("Average waiting time for customers who wait",
                   self.averageWaitTimeWhoWait,
                   self.averageQ1TimeWait,
                   self.averageQ2TimeWait)
        print h % ("Average service time",
                   self.averageServiceTime,
                   self.averageService1Time,
                   self.averageService2Time)

        h = "%60s:  %5d  %%           [ Q1: %4d %%         Q2: %4d %%       ]"
        print h % ("Probability a customer has to wait",
                   self.waitProbability * 100,
                   self.wait1Probability * 100,
                   self.wait2Probability * 100)

        h = "%60s:  %5.2f  minutes"
        print h % ("Average time between arrivals",
                   self.averageInterarrrivalTime)
        print h % ("Average time each customer spends in system",
                   self.averageSystemTime)

        # print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q2",
        #                           self.wait2Probability * 100)


def runTrials(numTrials=10, numCustomers=10, verbose=True):
    averageQ1Time = 0
    averageQ2Time = 0
    averageWaitingTime = 0
    averageWaitTimeWhoWait = 0
    averageQ1TimeWait = 0
    averageQ2TimeWait = 0
    averageServiceTime = 0
    averageService1Time = 0
    averageService2Time = 0
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
        averageWaitTimeWhoWait += trial.averageWaitTimeWhoWait
        averageQ1TimeWait += trial.averageQ1TimeWait
        averageQ2TimeWait += trial.averageQ2TimeWait
        averageServiceTime += trial.averageServiceTime
        averageService1Time += trial.averageService1Time
        averageService2Time += trial.averageService2Time
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
    averageWaitTimeWhoWait /= numTrials
    averageQ1TimeWait /= numTrials
    averageQ2TimeWait /= numTrials
    averageServiceTime /= numTrials
    averageService1Time /= numTrials
    averageService2Time /= numTrials
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
    # print "%60s:  %5.2f  minutes" % ("Average Q1 wait time", averageQ1Time)
    # print "%60s:  %5.2f  minutes" % ("Average Q2 wait time", averageQ2Time)
    # print
    print "%60s:  %5.2f  minutes     [ Q1:%5.2f minutes   Q2:%5.2f minutes ]" % ("Average waiting time for all customers", averageWaitingTime, averageQ1Time, averageQ2Time)
    print "%60s:  %5.2f  minutes     [ Q1:%5.2f minutes   Q2:%5.2f minutes ]" % ("Average waiting time for customers who wait", averageWaitTimeWhoWait, averageQ1TimeWait, averageQ2TimeWait)
    print "%60s:  %5.2f  minutes     [ Q1:%5.2f minutes   Q2:%5.2f minutes ]" % ("Average service time", averageServiceTime, averageService1Time, averageService2Time)
    print "%60s:  %5d  %%           [ Q1: %4d %%         Q2: %4d %%       ]" % ("Probability a customer has to wait", waitProbability * 100, wait1Probability * 100, wait2Probability * 100)
    print "%60s:  %5.2f  minutes" % ("Average time between arrivals", averageInterarrrivalTime)
    print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", averageSystemTime)
    # print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q1", wait1Probability * 100)
    # print "%60s:  %5d  %%" % ("Probability a customer has to wait in Q2", wait2Probability * 100)
    # print "%60s:  %5d  %%" % ("Percentage of time server is idle", idleProbability * 100)


def main():
    numTrials = 10
    numCustomersPerTrial = 10
    displayStats = True

    # run multiple trials and display averages
    runTrials(numTrials, numCustomersPerTrial, displayStats)

    # numCustomers = 10
    # sim = Simulation(numCustomers)
    # sim.display()

if __name__ == '__main__':
    main()
