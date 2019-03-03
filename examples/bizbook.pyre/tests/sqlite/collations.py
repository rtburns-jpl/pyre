#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    # access the packages
    import bizbook
    import operator

    # build a simple projection
    class titles(bizbook.db.query, book=bizbook.schema.Book):
        """A short query on the book table"""
        id = book.id
        title = book.title
        category = book.category
        price = book.price

    class collated(titles):
        """Extend the 'titles' query with a collation order"""
        # collation
        order = (titles.category, bizbook.db.descending(titles.price), titles.title)

    # build datastore
    db = bizbook.sqlite()

    # run the query
    report = list(db.select(collated()))
    # for record in report: print(record)
    # here is what we expect
    correct = sorted(
        sorted(
            sorted(db.select(titles), key=operator.attrgetter('title')),
            key=operator.attrgetter('price'), reverse=True),
        key=operator.attrgetter('category'))
    # check
    assert report == correct

    # grant access to the test parts
    return db, titles


# main
if __name__ == "__main__":
    test()


# end of file
