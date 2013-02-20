#!/usr/bin/env python

# (c) 2011 Rdio Inc
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from rdio import Rdio
from rdio_consumer_credentials import RDIO_CONSUMER_KEY, RDIO_CONSUMER_SECRET
from urllib2 import HTTPError

import csv, time

rdio = Rdio((RDIO_CONSUMER_KEY, RDIO_CONSUMER_SECRET))

try:

    # Authentication.
    url = rdio.begin_authentication('oob')
    print 'Go to: ' + url
    verifier = raw_input('Then enter the code: ').strip()
    rdio.complete_authentication(verifier)

    # Playlist initialization.
    my_playlists = rdio.call('getPlaylists', {
        'extras': 'trackKeys',
    })['result']['owned']

    playlist = None

    for pl in my_playlists:
        if pl['name'] == 'Pandora Likes':
            playlist = pl

    if playlist is None:
        playlist = rdio.call('createPlaylist', {
            'name': 'Pandora Likes',
            'description': 'Tracks imported from my Pandora likes.',
            'tracks': '',
        })
        playlist['trackKeys'] = []
        playlist['key'] = playlist['result']['key']
    
    # Harvest the Pandora likes.
    with open('tracks.txt', 'rb') as tracks_file:

        tracks_lines = tracks_file.readlines()
        tracks_count = len(tracks_lines)
        tracks = csv.reader(tracks_lines)
        track_ids = []

        for (counter, track) in enumerate(tracks):

            print '\n{} of {}: {}'.format(counter + 1, tracks_count, track[0])

            # Try and find this track on Rdio.
            search = rdio.call('search', {
                'query': track[0],
                'types': 'Track',
            })

            # If we have results, store the track ID for the first result.
            if search['result']['number_results'] > 0:

                track = search['result']['results'][0]

                print '     Found: {} -- {}'.format(
                    track['artist'].encode('ascii', 'ignore'),
                    track['name'].encode('ascii', 'ignore'),
                )

                # Don't include this track if it's already in the playlist.
                if track['key'] in playlist['trackKeys']:
                    print '   (ignoring track: already in playlist)'
                else:
                    track_ids.append(track['key'])

    # Add the harvested track IDs to the playlist.
    playlist = rdio.call('addToPlaylist', {
        'playlist': playlist['key'],
        'tracks': ','.join(track_ids),
    })

except HTTPError, e:
    print e.read()
