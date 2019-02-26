import abc

class BookReceptor(object):

    def __init__(self, books, cfgfilename=None):
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
        while self._rulesraw:
            self._define_curr_rule(self._rulesraw.pop())
            currstrategy, sorting_order = self._curr_rule
            sorted_books = currstrategy.sort(sorting_order)
        return sorted_books


    def _define_curr_rule(self, rawrule):
        sorting_order = 0
        r = rawrule.split(' ')
        if len(r) == 2:
            sorting_order = int(r[1]) == 1
        strategy_index = int(r[0]) - 1
        self._curr_rule = [self._strategies[strategy_index], sorting_order]


class BookSorter(abc.ABC):
    @abc.abstractmethod
    def sort(self, reverse=False):
        pass


class TitleSorter(BookSorter):

    def __init__(self, books):
        self._books = {}
        for b in books:
            self._books[b.title] = b

    def sort(self, reverse=False):
        sorted_titles = sorted(self._books.keys(), reverse=reverse)
        return [self._books[title] for title in sorted_titles]


class AuthorSorter(BookSorter):

    def __init__(self, books):
        self._books = {}
        for b in books:
            self._books[b.author] = b

    def sort(self, reverse=False):
        sorted_authors = sorted(self._books.keys(), reverse=reverse)
        return [self._books[author] for author in sorted_authors]


class EditionYearSorter(BookSorter):

    def __init__(self, books):
        self._books = {}
        for b in books:
            self._books[b.edition_year] = b

    def sort(self, reverse=False):
        edyears = [b.edition_year.lower() for b in self._books.values()]
        sorted_edyear = sorted(edyears, reverse=reverse)
        return [self._books[edyear] for edyear in sorted_edyear]

