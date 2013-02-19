Rdio Pandora Likes importer
===========================

A script to import Pandora Likes to an Rdio playlist.

## Harvesting Pandora likes

    Note: This is a little gritty, but I haven't found a better way to do this yet. If you have, please let me know via a [new issue](https://github.com/nicksergeant/rdio-pandora-likes-importer/issues/new).

1. Head to http://www.pandora.com/profile/likes/[[ username ]] to view your likes.
2. Click "Show more" a bunch of times until you can see all of your likes on the page (the "Show more" link will be gone).
3. Open up a JavaScript console and type:

    $tracks = $('div#track_like_pages div.section');
    for (var i = 0; i < $tracks.length; i++) {
        var t = $tracks.eq(i);
        var title = $.trim($('h3.normal', t).text());
        var artist = $.trim($('div.infobox-body p.s-0 a', t).eq(0).text());
        console.log(artist + ' -- ' + title);
    }

4. Copy the output to a text file for later parsing. This file will spit out your liked tracks in this format:

    Artist -- Track Title
