This is a workflow and Python script to import Pandora Likes to an Rdio playlist.

## Harvesting Pandora likes

**Note:** This is a little gritty, but I haven't found a better way to do this yet. If you have, please let me know via a [new issue](https://github.com/nicksergeant/rdio-pandora-likes-importer/issues/new).

1. Head to http://www.pandora.com/profile/likes/username to view your likes (replace with your username, of course).
2. Click "Show more" a bunch of times until you can see all of your likes on the page (the "Show more" link will be gone).
    If you would like to automate the "Show more" click, you can open the javascript console and type:

        $('.backstage .show_more').trigger('click');
        $("html, body").animate({ scrollTop: $(document).height() }, "fast");
    
    Each time you paste this in and press enter it will act as if you clicked show more and scrolled to the bottom of the page.

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

## Running the import script

1. Copy `rdio_consumer_credentials-template.py` to `rdio_consumer_credentials.py`.
2. Change the credentials in that file to your consumer key and secret as indicated by
your Rdio application (you can apply for one [here](http://developer.rdio.com/apps/register)).
3. Make sure your text file with tracks exported from Pandora are in `tracks.txt` in the
directory of this script.
4. Run `python rdio-import.py`
5. Visit the link to request authentication.
6. Enter the authentication PIN in your terminal.
7. Watch and wait.
8. Magic.
9. Profit.
