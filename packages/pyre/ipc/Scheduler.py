# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import operator
from time import time as now
from pyre.units.SI import second


# declaration
class Scheduler:
    """
    Support for invoking event handlers at specified times
    """


    # interface
    def alarm(self, interval, handler):
        """
        Schedule {handler} to be invoked after {interval} elapses. 

        parameters:
           {interval}: expected to be a dimensional quantity from {pyre.units} with units of
                       time
           {handler}: a function that accepts two arguments, the scheduler instance that
                       invoked the handler, and the current time
        """
        # create a new alarm instance
        alarm = self._alarm(time=now()+interval/second, handler=handler)
        # add it to my list
        self._alarms.append(alarm)
        # sort 
        self._alarms.sort(key=operator.attrgetter("time"), reverse=True)
        # and return
        return


    def poll(self):
        """
        Compute the number of seconds until the next alarm comes due.

        If there are no scheduled alarms, {poll} returns {None}; if alarms are overdue, it
        returns 0.
        """
        # the necessary information is in the last entry in my {_alarms}, since they are
        # always in descending order; try to grab it
        try:
            due = self._alarms[-1].time
        # if this raised an {IndexError}
        except IndexError:
            # no scheduled alarms
            return None
        # bound from below and return the number of seconds
        return max(0, due - now())


    def awaken(self):
        """
        Raise all overdue alarms by calling the registered handlers
        """
        # get my alarms
        alarms = self._alarms
        # get the time
        time = now()

        # iterate through my alarms
        while 1:
            # attempt
            try:
                # to grab one
                alarm = alarms.pop()
            # if none are left
            except IndexError:
                # all done
                return
            # if this alarm is not due yet
            if time < alarm.time:
                # put it back at the end of the list
                alarms.append(alarm)
                # no need to look any further
                break
            # otherwise, this alarm is overdue; invoke the handler
            alarm.handler(scheduler=self, timestamp=time)

        # all done
        return
        

    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # alarms are stored in a list that is always sorted in descending order on alarm time
        self._alarms = []

        return


    # implementation details
    # private types
    class _alarm:
        """Encapsulate the time and event handler of an alarm"""

        def __init__(self, time, handler):
            self.time = time
            self.handler = handler
            return

        __slots__ = ("time", "handler")


    # private data
    _alarms = None


# end of file 
