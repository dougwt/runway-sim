import argparse
import random
from customer import Customer


class Simulation():
    def __init__(self, numCustomers=100):
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
        for i in range(self.numCustomers):
            interarrivalTime, serviceTime = self.generateRandomValues()

            if (i == 0):
                prevEndTime = 0
            else:
                prevEndTime = self.queue[i-1].serviceTimeEnds

            customer = Customer(i+1, interarrivalTime, serviceTime, prevEndTime, self.clock)
            self.queue.append(customer)
            self.clock = customer.arrivalTime
        self.calculateStats()

    def generateRandomValues(self):
        interarrivalTime = self.determineServiceTime(random.randrange(1, 101))
        serviceTime = random.randrange(1, 9)
        # print "(" + str(interarrivalTime) + "," + str(serviceTime) + ")"
        return (interarrivalTime, serviceTime)

    def determineServiceTime(self, interarrivalRandom):
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
        # temporary variables used for calculating averages/etc
        totalWaitingTime = 0
        totalServiceTime = 0
        totalSystemTime = 0
        totalIdleTime = 0
        totalIterarrivalTime = 0
        totalSimulationTime = self.queue[-1].serviceTimeEnds
        numCustomersWhoWait = 0

        # iterate through each customer in the queue
        for customer in self.queue:
            totalWaitingTime += customer.waitingTimeInQueue
            totalIdleTime += customer.idleTime
            totalServiceTime += customer.serviceLength
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
        field_width = 10  # number of characters per field_width
        columns = 9  # number of columnds to be displayed

        # horizontal line
        print '-' * field_width * columns

        # 1st line of header column
        headers = ('Customer', 'InterArr', 'Arrival', 'Service', 'Begin', 'Waiting', 'End', 'System', 'Idle')
        headers = [i.center(field_width) for i in headers]
        print ''.join(headers)

        # 2nd line of header column
        headers = ['#']
        headers.extend(['Time'] * 8)
        headers = [i.center(field_width) for i in headers]
        print ''.join(headers)

        # horizontal line
        print '-' * field_width * columns

        # print row for each customer
        for customer in self.queue:
            print customer

        print
        print "%60s:  %5.2f  minutes" % ("Average waiting time for all customers", self.averageWaitingTime)
        print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", self.averageWaitingTimeWhoWait)
        print "%60s:  %5.2f  minutes" % ("Average service time", self.averageServiceTime)
        print "%60s:  %5.2f  minutes" % ("Average time between arrivals", self.averageInterarrrivalTime)
        print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", self.averageSystemTime)
        print "%60s:  %5d  %%" % ("Probability a customer has to wait in the queue", self.waitProbability * 100)
        print "%60s:  %5d  %%" % ("Percentage of time server is idle", self.idleProbability * 100)


def runTrials(numTrials=10, numCustomers=10, verbose=True):
    averageWaitingTime = 0
    averageWaitingTimeWhoWait = 0
    averageServiceTime = 0
    averageInterarrrivalTime = 0
    averageSystemTime = 0
    waitProbability = 0
    idleProbability = 0
    trials = []

    for i in range(numTrials):
        trial = Simulation(numCustomers)

        if (verbose):
            print
            print "Trial %d" % (i + 1)
            trial.display()

        trials.append(trial)

        averageWaitingTime += trial.averageWaitingTime
        averageWaitingTimeWhoWait += trial.averageWaitingTimeWhoWait
        averageServiceTime += trial.averageServiceTime
        averageInterarrrivalTime += trial.averageInterarrrivalTime
        averageSystemTime += trial.averageSystemTime
        waitProbability += trial.waitProbability
        idleProbability += trial.idleProbability

    averageWaitingTime /= numTrials
    averageWaitingTimeWhoWait /= numTrials
    averageServiceTime /= numTrials
    averageInterarrrivalTime /= numTrials
    averageSystemTime /= numTrials
    waitProbability /= numTrials
    idleProbability /= numTrials

    print
    print '-'*79
    print "Averages for %d Completed Trials (%d Customers per Trial):" % (numTrials, numCustomers)
    print '-'*79
    print "%60s:  %5.2f  minutes" % ("Average waiting time for all customers", averageWaitingTime)
    print "%60s:  %5.2f  minutes" % ("Average waiting time for customers who wait", averageWaitingTimeWhoWait)
    print "%60s:  %5.2f  minutes" % ("Average service time", averageServiceTime)
    print "%60s:  %5.2f  minutes" % ("Average time between arrivals", averageInterarrrivalTime)
    print "%60s:  %5.2f  minutes" % ("Average time each customer spends in system", averageSystemTime)
    print "%60s:  %5d  %%" % ("Probability a customer has to wait in the queue", waitProbability * 100)
    print "%60s:  %5d  %%" % ("Percentage of time server is idle", idleProbability * 100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("trials", help="the number of trials to run", type=int, default=10)
    parser.add_argument("customers", help="the number of customers in each trial", type=int, default=10)
    parser.add_argument("-v", "--verbose", help="display statistics for each trial", action="store_true")
    args = parser.parse_args()

    numTrials = 10
    numCustomersPerTrial = 10

    if args.trials >= 1:
        numTrials = args.trials

    if args.customers >= 2:
        numCustomersPerTrial = args.customers

    displayStats = args.verbose

    # run multiple trials and display averages
    runTrials(numTrials, numCustomersPerTrial, displayStats)

if __name__ == '__main__':
    main()
