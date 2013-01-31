---
layout: post
title: Development Reopens
---

I received some excellent feedback on the edus2 system regarding usability of the interface and system as a whole.  Glenn Verheul was having [issues](https://github.com/asclepius/edus2/issues/10) with the volume of scans he was using.  Scrollbars were added to the settings menu so the list isn't limited by the size of your screen anymore.  This was a bug I hadn't picked up simply because we didn't use as many scans.

Glenn mentioned some trouble deleting scans.  Has anyone else run into this?  Please email or comment.

To try the new changes for yourself try the following steps.

1. Copy your working edus2 directory into a back up just in case something goes wrong, this way your scan list won't be affected.  Change the ~/src/edus2 part to whatever directory you have your system in.

        cp -a ~/src/edus2 ~/src/edus2-backup

2. Update to the latest version from github

        cd ~/src/edus2
        git pull

3. Run it and check that your settings menu is now scrollable, if you have any problems email/comment and remember that you can run the simulator out of the backup directory you made.
