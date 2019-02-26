from book import Book
from abc import ABC, abstractmethod

class BookReceptor(object):

    def __init__(self, books, cfgfilename=None):
        self._books = books
        self._strategies = [TitleSorter(books), AuthorSorter(books), EditionYearSorter(books)]
        self._curr_rule = None
        self._rulesraw = None
        if cfgfilename is not None:
            conf_file = open(cfgfilename, 'r')
            self._rulesraw = [raw for raw in conf_file.readlines()]
            self._rulesraw.reverse()


    def sort(self):
        if self._rulesraw is None:
            '''Default sorting strategy, by title (TitleSorter)'''
            return self._strategies[0].sort()

        sorted_books = []
        limits = [0, len(self._books)]
        while self._rulesraw:
            self._define_curr_rule(self._rulesraw.pop())
            currstrategy, sorting_order = self._curr_rule
            sorted_books = currstrategy.sort(reverse=sorting_order)
            limits = currstrategy.equal_elements()
            if limits == []:
                break

        return sorted_books


    def _define_curr_rule(self, rawrule):
        sorting_order = 0
        r = rawrule.split(' ')
        if len(r) == 2:
            sorting_order = int(r[1]) == 1
        strategy_index = int(r[0]) - 1
        self._curr_rule = [self._strategies[strategy_index], sorting_order]


class BookSorter(ABC):

    @abstractmethod
    def sort(self, attrfunc, reverse=False):
        self._books = sorted(self._books, key=attrfunc, reverse=reverse)
        return self._books

    @abstractmethod
    def equal_elements(self, attrfunc):
        sublists_limits = []
        attrs = [attrfunc(b) for b in self._books]
        i = 0  # indicates the end of a sublist
        while i < len(attrs)-1:
            if attrs[i] == attrs[i+1]:
                start, i = self._sublist_limits(attrs, i)
                sublists_limits.append(start)
                sublists_limits.append(i)
            i += 1
        if sublists_limits == []:
            sublists_limits = [-1 -1]
        return sublists_limits


    def _sublist_limits(self, attrslist, index):
        attr = attrslist[index]
        limits = [index, index + 1]  # [start, end]
        i = limits[1] + 1 # indicates the new 'end'
        while (i < len(attrslist)-1) and (attrslist[i] == attr):
            limits[1] = i
            i += 1
        return limits


class TitleSorter(BookSorter):

    def __init__(self, books):
        self._books = books

    def sort(self, attrfunc=None):
        return super(TitleSorter, self).sort(Book.title, reverse, start, end)

    def equal_elements(self, attrfunc=None):
        return super(TitleSorter, self).equal_elements(attrfunc=Book.title)


class AuthorSorter(BookSorter):

    def __init__(self, books):
        self._books = books

    def sort(self, attrfunc=None, reverse=False):
        return super(AuthorSorter, self).sort(Book.author, reverse, start, end)

    def equal_elements(self, attrfunc=None):
        return super(AuthorSorter, self).equal_elements(attrfunc=Book.author)


class EditionYearSorter(BookSorter):

    def __init__(self, books):
        self._books = books

    def sort(self, attrfunc=None, reverse=False):
        return super(EditionYearSorter, self).sort(Book.edition_year, reverse, start, end)

    def equal_elements(self, attrfunc=None):
        return super(EditionYearSorter, self).equal_elements(attrfunc=Book.edition_year)

