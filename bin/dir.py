#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import os
import re
import subprocess
# support
import pyre


# the app
class Dir(pyre.application):
    """
    A generator of colorized directory listings that is repository aware
    """


    # user configurable state
    across = pyre.properties.bool(default=False)
    across.doc = "sort multi-column output across the window"

    # protocol obligations
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # build the list of directories
        directories = list(self.argv) or ['.']
        # figure out how many there are
        args = len(directories)

        # save the currnet working directory
        cwd = os.getcwd()

        # go through each on
        for directory in directories:
            # if there is more than one
            if args > 1:
                # show the one being dumped
                print(f"{directory}:")
            # go there
            os.chdir(directory)
            # get the listing
            text = "\n".join(self.render())
            # and if it's non-trivial
            if text:
                # print it
                print(text)
            # if necessary
            if args > 1:
                # print a separator
                print()
            # come back
            os.chdir(cwd)

        # all done
        return 0


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # attach my terminal
        self.terminal = self.executive.terminal
        # all done


    # implementation details
    def render(self):
        """
        Generate the directory listing
        """
        # get the terminal
        terminal = self.terminal
        # decorate the directory contents
        entries = self.colorize()

        # figure out the width of the terminal
        width = terminal.width
        # deduce the layout
        layout = (1,0) if self.across else (0,1)
        # make a tabulator
        tabulator = Table(width=width, layout=layout, entries=entries)
        # get the grid
        grid = tabulator.grid
        # unpack its shape
        rows, columns = grid.tile.shape
        # ask for the column width
        columnWidth = tabulator.width

        # get the reset code from the terminal
        reset = terminal.ansi["normal"]

        # go through the rows
        for row in range(rows):
            # initialize the pile
            fragments = []
            # go through the columns
            for col in range(columns):
                # get the entry
                entry = grid[(row, col)]
                # render it
                fragments.append(entry.render(reset=reset))
                # every column other than the last
                if col < columns-1:
                    # adds a bit of padding
                    fragments.append(" "*(columnWidth - (len(entry.name)+len(entry.marker))))
            # put it all together
            yield "".join(fragments)

        # all done
        return


    def colorize(self):
        """
        Walk the directory contents through the various colorizers
        """
        # make the listing
        entries = self.discover()
        # run it through the git colorizer
        entries = self.git(entries=entries)
        # and return them
        return entries


    def git(self, entries):
        """
        Decorate the directory {entries} with information from the local git repository
        """
        # make a git aware colorizer
        git = Git(terminal=self.terminal)
        # run {entries} through it
        yield from git.colorize(entries)
        # all done
        return


    def discover(self):
        """
        Initialize the directory listing
        """
        # mount the filesystem
        fs = pyre.filesystem.local(root='.')
        # expand the top level only
        fs.discover(levels=1)

        # get the names and info nodes of the contents of the current working directory
        for name in sorted(fs.contents.keys()):
            # get the associated node
            node = fs[name]
            # and the associated meta-data
            info = fs.info(node=node)
            # make an entry
            entry = Entry()
            # set the name
            entry.name = name
            # decorate based on the file type
            info.identify(explorer=self, entry=entry)
            # publish it
            yield entry

        # all done
        return


    # callbacks for identifying file types
    def onBlockDevice(self, entry, info):
        """
        Decorate block devices
        """
        # mark it
        entry.marker = '\u2584'
        # all done
        return entry


    def onCharacterDevice(self, entry, info):
        """
        Decorate character devices
        """
        # mark it
        entry.marker = "#"
        # all done
        return entry


    def onFile(self, entry, info):
        """
        Decorate regular files
        """
        # if the user has execute permissions
        if info.mode(entity=info.user, access=info.execute):
            # mark it
            entry.marker = "*"
        # all done
        return entry


    def onFolder(self, entry, info):
        """
        Decorate folders
        """
        # mark it
        entry.marker = "/"
        # all done
        return entry


    def onLink(self, entry, info):
        """
        Decorate symbolic links
        """
        # mark it
        entry.marker = '@' #"\u2192"

        # if the link is broken
        if info.referent is None:
            # colorize the marker
            entry.markerColor = self.terminal.rgb(rgb="c02020")
        # all done
        return entry


    def onNamedPipe(self, entry, info):
        """
        Decorate named pipes
        """
        # mark it
        entry.marker = "|"
        # all done
        return entry


    def onSocket(self, entry, info):
        """
        Decorate sockets
        """
        # mark it
        entry.marker = "="
        # all done
        return entry


# helpers
class Entry:
    """
    The information necessary for rendering a directory entry
    """


    # public data
    name = ""
    marker = ""
    nameColor = ""
    markerColor = ""


    # interface
    def render(self, reset):
        """
        Render me
        """
        # collect the fragments
        label = [
            self.nameColor, self.name, reset,
            self.markerColor, self.marker, reset
        ]
        # assemble
        return "".join(label)


class Table:
    """
    The builder of the listing layout
    """


    # public data
    grid = None


    # meta-methods
    def __init__(self, entries, width, layout=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # make the grid, which adjust my shape and width as a side effect
        self.grid = self.makeGrid(maxWidth=width, layout=layout, entries=entries)
        # all done
        return


    # implementation details
    def makeGrid(self, maxWidth, entries, layout):
        """
        Make a grid out of the directory {entries}
        """
        # realize the container
        data = tuple(self.tabulate(maxWidth=maxWidth, entries=entries))
        # which deduces the table shape as a side effect
        shape = self.shape
        # get the grid factory
        import pyre.grid
        # make one
        grid = pyre.grid.grid(shape=shape, layout=layout, data=data)
        # and return it
        return grid


    def tabulate(self, maxWidth, entries):
        """
        Generate the entry container and its shape
        """
        # initialize the stats
        longestName = 0
        longestMarker = 0
        numEntries = 0

        # go through the entries
        for entry in entries:
            # update the size
            numEntries += 1
            # update the longest name
            longestName = max(longestName, len(entry.name))
            # and the longest marker
            longestMarker = max(longestMarker, len(entry.marker))
            # publish
            yield entry

        # if there were no entries
        if numEntries == 0:
            # make a trivial shape
            self.shape = (0,0)
            # and bail
            return

        # compute the minimum width of a column, accounting for my file type marker and a margin
        minWidth = longestName + longestMarker + 2
        # the grid width
        columns = max(min(maxWidth // minWidth, numEntries), 1)
        # and the grid height
        lines = numEntries // columns + (1 if numEntries % columns else 0)

        # record the minimum required column width
        self.width = minWidth
        # set the shape
        self.shape = (lines, columns)

        # pad with blank entries
        yield from [Entry()]*(lines*columns - numEntries)

        # all done
        return


    # private data
    width = 0
    shape = None


class Git:
    """
    Extract the status of the current git worktree and colorize matching directory entries
    """


    # interface
    def colorize(self, entries):
        """
        Colorize the directory {entries} with info from the current worktree
        """
        # get the root of the worktree
        root = self.root()
        # if we are not in a git worktree
        if root is None:
            # pass the entries through untouched
            yield from entries
            # and bail
            return
        # get the current working directory
        cwd = pyre.primitives.path.cwd()
        # attempt to
        try:
            # compute the prefix
            prefix = cwd.relativeTo(root)
        # should be impossible, but just in case something went wrong
        except ValueError as error:
            # this is a perfect case for a firewall
            import journal
            # so make one
            journal.firewall("dir").log(str(error))
            # pass the entries through untouched
            yield from entries
            # and bail
            return

        # ask git for status info
        info = self.status(prefix=prefix)

        # now, go through the entries
        for entry in entries:
            # grab the name
            name = entry.name

            # if the entry is a file with conflicts
            if name in info.conflicted:
                # adjust its color
                entry.nameColor = self.palette["conflicted"]
            # if the entry has changed since it were added to the index
            elif name in info.unstaged and name in info.staged:
                # adjust its color
                entry.nameColor = self.palette["staged-modified"]
            # if the entry has changed but not added to the index
            elif name in info.unstaged:
                # adjust its color
                entry.nameColor = self.palette["unstaged"]
            # if the entry is a staged file
            elif name in info.staged:
                # adjust its color
                entry.nameColor = self.palette["staged"]
            # if the entry is an untracked file
            elif name in info.untracked:
                # adjust its color
                entry.nameColor = self.palette["untracked"]
            # if the entry is an ignored file
            elif name in info.ignored:
                # adjust its color
                entry.nameColor = self.palette["ignored"]

            # the rest go through unharmed
            yield entry

        # all done
        return


    # meta-methods
    def __init__(self, terminal, **kwds):
        # chain up
        super().__init__(**kwds)
        # make the dispatch table
        self.dispatcher = {
            "no_commits": self.noCommits,
            "tracking": self.tracking,
            "moved": self.moved,
            "changed": self.changed,
        }
        # colors
        self.palette = {
            "conflicted": terminal.x11["firebrick"],
            "ignored": terminal.gray["gray30"],
            "staged": terminal.x11["dark_sea_green"],
            "staged-modified": terminal.x11["indian_red"],
            "unstaged": terminal.misc["amber"],
            "untracked": terminal.x11["steel_blue"],
        }

        # all done
        return


    # implementation details
    def root(self):
        """
        Locate the root of the git worktree
        """
        # set up the command
        cmd = [ "git", "rev-parse", "--show-toplevel" ]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # if there was no error
            if git.returncode == 0:
                # read the location of the repository root
                root = stdout.strip()
                # turn into a path and return it
                return pyre.primitives.path(root)
        # all done
        return None


    def status(self, prefix):
        """
        Collect the status of the worktree
        """
        # set up the command
        cmd = [
            "git", "status",
            "--porcelain",
            "--branch", "--untracked", "--ignored=traditional",
            "."]
        # settings
        options = {
            "executable": "git",
            "args": cmd,
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "universal_newlines": True,
            "shell": False }
        # invoke
        with subprocess.Popen(**options) as git:
            # collect the output
            stdout, stderr = git.communicate()
            # if there was an error
            if git.returncode != 0:
                # this is not a git repository, so we are done
                return
            # extract the output
            report = stdout.splitlines()
            # otherwise, parse the output and return it
            return self.parse(prefix=prefix, report=report)
        # if something went wrong, return an empty summary
        return GitInfo()


    def parse(self, prefix, report):
        # make an info table
        table = GitInfo()
        # go through the lines in {report}
        for line in report:
            # attempt to match it
            match = self.parser.match(line)
            # if we couldn't
            if match is None:
                # ignore and move on
                continue
            # get the enclosing group name
            case = match.lastgroup
            # look up the handler and dispatch
            self.dispatcher[case](table=table, prefix=prefix, match=match)
        # all done
        return table


    def noCommits(self, table, match, **kwds):
        """
        Extract the branch name of a newly created repository
        """
        # set the branch name
        table.local = match.group("new")
        # all done
        return table


    def tracking(self, table, match, **kwds):
        """
        Extract the branch name from a repository that tracks a remote one
        """
        # get the match group dictionary
        info = match.groupdict()
        # set the branch name
        table.local = info["local"]
        table.remote = info["remote"]
        table.ahead = 0 if info["ahead"] is None else int(info["ahead"])
        table.behind = 0 if info["behind"] is None else int(info["behind"])
        # all done
        return table


    def moved(self, table, match, **kwds):
        """
        Compute the number of moved files
        """
        # all done
        return table


    def changed(self, table, prefix, match):
        """
        Compute the number of changed files
        """
        # get the match group dictionary
        info = match.groupdict()
        # get the code
        code = info["CODE"]
        # and the filename
        filename = pyre.primitives.path(info["filename"])
        # project it onto the {prefix} and pull out the top
        entry = filename.relativeTo(prefix)[0]

        # if this is an untracked file
        if code in self.untracked:
            # add it to the pile
            table.untracked.add(entry)
            # all done
            return table

        # if this is an ignored file
        if code in self.ignored:
            # add it to the pile
            table.ignored.add(entry)
            # all done
            return table

        # if this is a conflict indicator
        if code in self.conflicts:
            # add it to the pile
            table.conflicted.add(entry)
            # all done
            return table

        # if the code has any info on the index side
        if code[0] != ' ':
            # add it to the staged pile
            table.staged.add(entry)

        # if the code has any info on the worktree side
        if code[1] != ' ':
            # add it to the staged pile
            table.unstaged.add(entry)

        # all done
        return table


    # private data
    parser = re.compile("|".join([
        # brand new repositories without any commits
        r"(?P<no_commits>## No commits yet on (?P<new>.+))$",
        # repositories at a known branch
        r"(?P<tracking>## " +
            # the local branch name
            r"(?P<local>\w+)" +
            r"(" +
                # the remote branch name
                r"\.\.\.(?P<remote>[\w/]+)" +
                # divergence information
                r"(" +
                    r" \[(ahead (?P<ahead>\d+))?(, )?(behind (?P<behind>\d+))?\]" +
                r")?" +
            r")?" +
        r")$",
        # files that have been copied/renamed
        r"(?P<moved>(?P<code>..) (?P<source>.+) -> (?P<destination>.+))$",
        # files with modifications
        r"(?P<changed>(?P<CODE>..) (?P<filename>.+))$"
    ]))


    # git status code sets
    untracked = { "??" }
    ignored = { "!!" }
    conflicts = { "DD", "AU", "UD", "UA", "DU", "AA", "UU" }


class GitInfo:
    """
    Aggregator of information about the worktree status
    """

    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the branch info
        self.local = None
        self.remote = None
        self.ahead = 0
        self.behind = 0
        # build the file categories
        self.conflicted = set()
        self.staged = set()
        self.unstaged = set()
        self.ignored = set()
        self.untracked = set()

        # all done
        return


    # debugging support
    def dump(self):
        """
        Show me
        """
        print(f"git info:")
        print(f"  branch info:")
        print(f"    local: {self.local}")
        print(f"    remote: {self.remote}")
        print(f"    ahead: {self.ahead}")
        print(f"    behind: {self.behind}")

        print(f"  file info:")
        print(f"    ignored:")
        for entry in self.ignored:
            print(f"      {entry}")
        print(f"    untracked:")
        for entry in self.untracked:
            print(f"      {entry}")
        print(f"    conflicted:")
        for entry in self.conflicted:
            print(f"      {entry}")
        print(f"    unstaged:")
        for entry in self.unstaged:
            print(f"      {entry}")
        print(f"    staged:")
        for entry in self.staged:
            print(f"      {entry}")

        return


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Dir(name="dir")
    # invoke
    status = app.run()
    # share
    raise SystemExit(status)


# end of file