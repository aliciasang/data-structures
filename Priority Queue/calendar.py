from PriorityQueue import *

from dataclasses import dataclass
import datetime
import re

######################################################################
''' simple class to implement an Event class for the Calendar, having
    two fields, datetime and description '''
@dataclass
class Event:
    datetime: str = "2025.04.04.23:59"
    desc:     str = "arbitrary event"

    def __str__(self) -> str:
        yr, mo, day, time = self.datetime.split('.')
        return f"{yr}/{mo}/{day} @ {time}: {self.desc}"

######################################################################
class Calendar:
    ''' Calendar class using a priority queue to store events. '''
    __slots__ = ('_events')
    
    def __init__(self):
        self._events: PriorityQueue[str,str] = PriorityQueue()

    def validate(self, datetime_str: str) -> bool:
        ''' validate a string versus the "yyyy.mm.dd.hh:mm" format
        Parameters:
            datetime_str: input string to be validated
        Returns:
            True should the datetime_str be validated
        Raises:
            ValueError: If the input string does not match the expected format.
        '''
        pattern = re.compile(r'^\d{4}\.\d{2}\.\d{2}\.\d{2}:\d{2}$')
        if not pattern.match(datetime_str):
            raise ValueError("Invalid datetime format. Expected 'yyyy.mm.dd.hh:mm'.")

        year, month, day, time = datetime_str.split('.')
        hour, minute = time.split(':')
        if not (1 <= int(month) <= 12 and 1 <= int(day) <= 31 and \
                0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
            raise ValueError("Invalid datetime values.")
        # not handling leap years
        if (int(month) in [4,6,9,11] and int(day) > 30) or \
           (int(month) == 2          and int(day) > 28):
            raise ValueError("Invalid day for given month.")

        return True
    
    def addEvent(self, datetime: str = "2025.05.01:14:00", desc: str = "example event") -> None:
        ''' adds a new event to the calendar using a given time and event description
        Parameters:
            datetime: string in format "yyyy.mm.dd.hh:mm" where hh is in 24-hour format
            desc: string describing the event
        Raises:
            ValueError if the datetime string does not match the expected format
        '''
        self.validate(datetime)
        self._events.insert(datetime, desc)
    
    def getNextEvent(self) -> Event:
        ''' removes and returns the next event from the calendar
        Returns:
            an Event object with datetime and desc attributes
        Raises:
            EmptyError if the calendar is empty
        '''
        pq_entry = self._events.removeMin()
        event = Event(datetime = pq_entry.key, desc = pq_entry.value)
        return event

    def min(self) -> Event:
        ''' returns (a copy of) the minimum event from the calendar
        Returns:
            an Event object with datetime and desc attributes
        Raises:
            EmptyError if the calendar is empty
        '''
        pq_entry = self._events.min()
        event = Event(datetime = pq_entry.key, desc = pq_entry.value)
        return event
    
    def __str__(self) -> str:
        ''' return a pretty-print format for the calendar
        Returns:
            a string version of the calendar
        '''
        events_str = "Calendar Of Events:\n"
        # use the string returned by PriorityQueue to build up what to
        # print here
        tuples_str = str(self._events)[1:-1]
        import ast
        events: list[tuple[str,str]] = list(ast.literal_eval("[" + tuples_str + "]"))
        for entry in events:
            event = Event(entry[0], entry[1])
            events_str += f"{event}\n"
        max_line_len = len(max(events_str.split('\n'), key=len))
        events_str  = ('>' * max_line_len) + '\n' + events_str
        events_str += ('<' * max_line_len)
        return events_str

    def removePastEvents(self) -> None:
        ''' removes any events from the calendar that are earlier than the
            current system time '''
        now = datetime.datetime.now().strftime("%Y.%m.%d.%H:%M")
        while not self._events.isEmpty() and self._events.min().key < now:
            self._events.removeMin()  # just discard

###############################
def main_for_testing() -> None:
    calendar = Calendar()
    calendar.addEvent("2025.06.04.17:15", "event A")
    calendar.addEvent("2025.06.04.17:16", "event B")
    calendar.addEvent("2025.06.04.17:14", "event C")

    print(calendar)
    print(f"min event is: {calendar.min()} [should be 'event C']")
    print(f"removing the min event...")
    event: Event = calendar.getNextEvent()
    print(calendar)
    print(f"inserting a new event...")
    calendar.addEvent("2025.06.04.12:00", "event D")
    print(calendar)
    print(f"min event is: {calendar.min()} [should be 'event D']")
    print(f"removing the min event...")
    event: Event = calendar.getNextEvent()
    print(f"min event is: {calendar.min()} [should be 'event A']")
    print(f"removing the min event...")
    event: Event = calendar.getNextEvent()
    print(f"min event is: {calendar.min()} [should be 'event B']")
    print(f"removing the min event...")
    event: Event = calendar.getNextEvent()
    try:
        event: Event = calendar.getNextEvent()
    except EmptyError as error:
        print(f"Correctly caught exception: {error}")

##################
def main() -> None:
    calendar = Calendar()

    done = False
    while not done:
        print("-------------------")
        print("Calendar Menu:")
        print("1. Print Calendar")
        print("2. Insert New Event")
        print("3. Show Next Event")
        print("4. Remove Next Event")
        print("5. Exit")
        print("-------------------")

        choice = input("Enter your choice: ")

        ######################
        if choice[0] == "1":
            # remove any old events first
            calendar.removePastEvents()
            print(calendar)
        ######################
        elif choice[0] == "2":
            good_date = False
            while not good_date:
                try: 
                    datetime_str = input("Enter event date/time (yyyy.mm.dd.hh:mm): ")
                    calendar.validate(datetime_str)
                except ValueError as err:
                    print(err)
                else:
                    good_date = True
            description  = input("Enter event description: ")
            calendar.addEvent(datetime_str, description)
        ######################
        elif choice[0] == "3":
            # remove any old events first
            calendar.removePastEvents()
            try: 
                next_event: Event = calendar.min()
                pad = '+' * len(str(next_event))
                print(pad + '\n' + str(next_event) + '\n' + pad)
            except EmptyError:
                print("No upcoming events....")
        ######################
        elif choice[0] == "4":
            # remove any old events first
            calendar.removePastEvents()
            try:
                next_event: Event = calendar.getNextEvent()
                print(f"Removed from calendar: {next_event}")
            except EmptyError:
                print("No events to remove....")
        ######################
        elif choice[0].lower() in ["5", 'x', 'q']:
            done = True
        ######################
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    #main_for_testing()
    main()
