#! /usr/bin/python3
import datetime
import pickle
import sys
import os

helptext = '''
ToDo application.
-----------------
A simple todo application.

An item is an entry. It has a text. It can have a deadline.
It is either pending or not. It has a creation date and a
completion date. These may be used to generate satistics.

A workList is an ordered collection of items. It has a
title and a creation date.

Multiple worklists are supported.

USEAGE
------

from the command line.
td [option] <arguments>

The options are
    al      Create a list. Takes N arguments and switches current
            list to the last one.
            <list1> <list2> <list3> ... <listN>
    dl      Deletes the current list.
    cl      Changes current list to given name.Takes one argument
            <list_name>
    a       Add an item to current list. Takes one argument + one optional
            <item string> <yyyy/mm/dd>
    d       Deletes an item from the current list. Takes N arguments
            <item_index> <item_index> ... <item_index>
    m       Marks an item in current list as done.Takes N arguments
            <item_index> <item_index> ... <item_index>
    s       Sync with online resource.

    -h
    --help  Display this help text and exit
'''


class Item:
    '''An item in a list.Provides data along with
    metadata capabilities'''
    def __init__(self, string, deadline=None):
        '''Initiate an item with data'''
        self.string = string
        self.__deadline = deadline
        self.__pending = True
        self.__created_at = datetime.datetime.now()
        self.last_touch = datetime.datetime.now()
        # string for pretty print--reset upon change to item
        # completed at is also implemented upon mark done
        self.__stamp__()

    def __stamp__(self):
        '''Stamps self for access using system times.
        Remember that syncing between timezone unaware
        machines will cause unexpected behaviour.
        Keep your server on the same clock as yourself.'''
        self.last_touch = datetime.datetime.now()
        self.__string = None
        self.__string = self.__str__()

    def __str__(self):
        '''Pretty print the item.Implements laziness to not eat cpu'''
        # check for an already existing string
        if self.__string is not None:
            return self.__string
        # if None then recompute and return
        string = ''
        # is it pending
        if self.__pending:
            string += '[ ]'
        else:
            string += '[X]'
        # space
        string += ' '
        # deadline
        if self.__deadline is None:
            string += '--------------------------'
        else:
            string += self.__deadline.__str__()
        # space
        string += ' '
        # text
        string += self.string
        return string

    def pending(self):
        '''Returns True if task is pending
        else returns False'''
        if self.__pending:
            return True
        return False

    def time_left(self):
        '''Returns a datetime difference to the deadline
        if it exists. None otherwise.
        If the task is marked done or deadline is crossed
        returns None'''
        if not self.__pending:
            return None
        now = datetime.datetime.now()
        if self.__deadline < now:
            return None
        # now that the task is pending and deadline has not been crossed
        return self.__deadline-now

    def mark_done(self):
        '''Marks the task done and generates some data for statistical use'''
        self.__pending = False
        now = datetime.datetime.now()
        self.__completed_at = now
        self.__stamp__()


class WorkList:
    '''A list of things to do'''
    def __init__(self, title):
        '''Initiate a list with title'''
        self.title = title
        self.created_on = datetime.datetime.now()
        self.__items = []

    def __getitem__(self, index):
        '''Returns the item at index specified'''
        return self.__items[index]

    def __str__(self):
        '''Pretty print the list.'''
        string = '-' * len(self.title)
        string += '\n'
        string += self.title+'\n'
        string += '-' * len(self.title)
        string += '\n'
        # add the created on date
        datestring = 'Created on: '+self.created_on.__str__() + '\n'
        string += datestring
        string += '-' * len(datestring)
        string += '\n'
        max_length = len(self.__items)
        for index, item in enumerate(self.__items):
            string += str(index).zfill(max_length) + ' ' + item.__str__() + '\n'
        return string

    def add_item(self, string, deadline=None):
        '''Add a new item with given parameters'''
        x = Item(string, deadline)
        self.__items.append(x)

    def mark_done(self, index):
        '''Marks the item at specified index as done'''
        self.__items[index].mark_done()

    def delete_item(self, index):
        '''Deletes the item at specified index'''
        self.__items.pop(index)


class Oauth:
    '''Implement Oauth for the website'''


class Todo:
    '''A todo application object'''
    def __init__(self):
        '''Initiate the todo application object with user credentials'''
        self.__lists = {}
        self.__current_list = None

    def save(self, path='tdrc'):
        '''saves all the lists'''
        # implement something like a pickle
        f = open(path, 'wb')
        pickle.dump([self.__lists, self.__current_list], f)
        f.close()

    def load(self, path='tdrc'):
        '''loads the object as per details listed in the config path.'''
        # implement loading.
        f = open(path, 'rb')
        self.__lists, self.current_list = pickle.load(f)
        f.close()

    def create_list(self, list_title):
        '''Create a new list with the list_title and switch current to it'''
        new_list = WorkList(list_title)
        self.__lists[list_title] = new_list
        self.change_list(list_title)

    def change_list(self, list_title):
        '''Changes current working list to list_title'''
        self.__current_list = self.__lists[list_title]

    def delete_list(self, list_title):
        '''Deletes the list with list_title'''
        self.__lists.pop(list_title)

    def add_item(self, string, deadline=None):
        '''Adds an item with a deadline to the current list'''
        self.__current_list.add_item(string, deadline)

    def mark_done(self, index):
        '''Marks the item in the current list with index specified as done'''
        if isinstance(index) != isinstance(0):
            infex = int(index)
        self.__current_list.mark_done(index)

    def delete_item(self, index):
        '''Deletes the item in the current list with index specified as done'''
        if isinstance(index) != isinstance(0):
            infex = int(index)
        self.__current_list.delete_item(index)

    def __getitem__(self, list_title):
        '''Returns the list with given title'''
        return self.__lists[list_title]

    def __str__(self):
        '''Prints the current lists'''
        return self.__current_list.__str__()

    def sync(self):
        '''Sync the lists with the online versions'''
        # need to implement Oauth and syncing techniques
        #
        # authenticate with the website
        # retrieve the website lists
        # for every list
        #   for every item
        #       copare with current data
        #       choose most recent timestamped data
        #       add to new list
        #   append new list to new database
        # overwrite both local and cloud with new database


def test():
    '''Tests the todo application for functionality'''
    t = Todo()
    t.save()
    t.create_list('general')
    t.add_item('read OAuth2.0')
    print(t)
    t.save()


def main():
    '''The main function for being called by command line'''
    td = Todo()
    args = sys.argv
    # remove the first arg as that is command name
    args = args[1:]
    # check if nothing was provided
    if len(args) == 0:
        print(helptext)
        return 0
    opt = args[0]
    parameters = args[1:]
    # now call based on options
    # check for help
    if (opt == 'h') or (opt == 'help'):
        print(helptext)
    # Sync
    if opt == 's':
        td.sync()
    # create a list
    if opt == 'al':
        for p in parameters:
            td.create_list(p)
    # delete a list
    if opt == 'dl':
        for p in parameters:
            td.delete_list(p)
    # current list
    if opt == 'cl':
        if len(parameters) == 1:
            td.change_list(parameters[0])
        else:
            return 1
    # add item to current list
    if opt == 'a':
        if len(parameters) == 2:
            string, dt = parameters
            y, m, d = [i for i in map(int, dt.strip().split('/'))]
            date = datetime.datetime(y, m, d)
            td.add_item(string, date)
        elif len(parameters) == 1:
            string = parameters[0]
            td.add_item(string)
        else:
            return 1
    # delete item
    if opt == 'd':
        for p in parameters:
            td.delete_item(p)
    # mark done
    if opt == 'm':
        for p in parameters:
            td.mark_done(p)
    # if no errors have occured.
    return 0
if __name__ == '__main__':
    sys.exit(main())
