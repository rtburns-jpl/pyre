# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved


# superclass
from .Device import Device
# the palette definitions
from . import palettes


# write message to a stream
class Stream(Device):
    """
    Journal device that writes messages to a stream
    """


    # types
    from .Memo import Memo
    from .Alert import Alert


    # interface
    def alert(self, entry):
        """
        Generate an alert.

        Alerts are user-facing; they are generated by {info}, {warning}, and {error}
        """
        # invoke the alert renderer to format the message
        content = self.alertRenderer.render(palette=self.palette, entry=entry)
        # and record it
        self.record(page=content)
        # all done
        return self


    def memo(self, entry):
        """
        Issue a memo

        Memos are developer-facing; they are generated by {debug} and {firewall}
        """
        # invoke the memo renderer to format the message
        content = self.memoRenderer.render(palette=self.palette, entry=entry)
        # and record it
        self.record(page=content)
        # all done
        return self


    def close(self):
        """
        Close the associated stream
        """
        # delegate
        self.stream.close()
        # all done
        return self


    # metamethods
    def __init__(self, stream, name="stream",
                 palette=palettes.null, alerts=None, memos=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # save the stream
        self.stream = stream
        # save the palette
        self.palette = palette
        # save the renderers
        self.memoRenderer = memos if memos is not None else self.Memo()
        self.alertRenderer = alerts if alerts is not None else self.Alert()

        # save the palette
        self.palette = palette

        # all done
        return


    # implementation details
    def record(self, page):
        """
        Record a message
        """
        # assemble the content
        content = "\n".join(page)
        # if there is anything there
        if content:
            # inject it
            print(content, file=self.stream)
        # all done
        return


# end of file
