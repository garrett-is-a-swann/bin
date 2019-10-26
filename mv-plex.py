#!/usr/bin/python3.6
import os
import re
import sys
import argparse

'''
Bulk move files from A-B, specifically for renaming to plex's naming convention of `SHOW TITLE - S##E##`
The most basic example is to use as such:
    $ py-mv --title "Yu Yu Hakusho" --format "e(\d{1,3})s" --season-start 1 26 67 95 --pad 2
to move files like ["Yu Yu Hakusho - e99s4.mkv", "Yu Yu Hakusho - e114s4.mkv", "Yu Yu Hakusho - e1s4.mkv"] to their correct names.

Use --dry-run to do a non-destructive test run.

Works with bash piping, ie: 
    $ ls | grep "How I Met Your Mother" | py-mv ...
'''

parser = argparse.ArgumentParser(description='Bulk move filenames while maintaining a naming convention.')
parser.add_argument('--title', type=str, dest='title',
        help='the name of the show')
parser.add_argument('--format', '--episode-regex', type=str, dest='format',
        help='the regex to extract the episode number')
parser.add_argument('--season-start', type=int, dest='season_starts', default=[1], nargs='+', 
        help='the starting episode for each season', metavar='ep')
parser.add_argument('--dry-run', dest='is_test', action='store_true', default=False,
        help='if present, perform a non-destructive test run and print what would occur to stdout.');
parser.add_argument('--ext', type=str, dest='file_ext',
        help='explicitly give the file extension to use. defaults to /\.[^.]*$/')
#TODO: This option? dunno if necessary
#parser.add_argument('--episode-range', dest='episode_slice', nargs='+', action=required_length(2), type=int, help='only rename a slice of the files', metavar='ep');
parser.add_argument('--pad', type=int, dest='pad_width', default=0, 
        help='width to 0-pad episodes', metavar='N');
parser.add_argument('--initial-season', type=int, dest='initial_season', default=1, 
        help='initial season with which to start increments.')

def required_length(nmin,nmax = None):
    if nmax == None:
        nmin, nmax = nmax, nmin
    class RequiredLength(argparse.Action):
        def __init__(self, *args, **kwargs):
            super(RequiredLength, self).__init__(*args, **kwargs)
        def __call__(self, parser, args, values, option_string=None):
            if not ((nmin == None or nmin<=len(values)) and len(values)<=nmax):
                parser.error(f'argument "{self.dest}" requires between {nmin} and {nmax} arguments')
            setattr(args, self.dest, values)
    return RequiredLength

def main(args, ls=None):
    if ls == None:
        ls = os.listdir()
    episode_list = []
    for name in ls:
        mv = move(name, **vars(args))
        if mv != None: 
            episode_list.append(mv)

    if args.is_test:
        episode_list.sort(key=lambda x: x[1])
        for episode in episode_list:
            print(f'mv "{episode[0]}" "{episode[1]}"')
    else:
        for episode in episode_list:
            os.rename(episode[0], episode[1]);

def move(name, title, format, season_starts, pad_width, file_ext, *args, **kwargs):
    match = re.search(format, name)
    if not match: 
        return None

    episode = int(match.group(1))
    season = 1
    for ep in season_starts:
        if episode >= ep:
            season = season_starts.index(ep) + 1

    strify = lambda e: str(e).rjust(pad_width, "0");
    if file_ext == None:
        file_ext = re.search('\.[^.]*$', name).group(0)

    return (name, f'{title} - S{strify(season)}E{strify(episode)}{file_ext}')

if __name__ == '__main__':
    args = parser.parse_args();
    main(args, None if sys.stdin.isatty() else [ line[:-1]for line in sys.stdin ])
