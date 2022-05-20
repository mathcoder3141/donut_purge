# Locally Optimistic Donut Purge:

A high level function of the script within the repo is to kick people out of the channel who don't participate in a given amount of days. This is to clear out the non-responders as well as increase the 1:1 pairing meetings that actually take place.

Donut automatically removes people if they are no-shows 3 times in a row but that doesn't seem to be enough

v1: Do this manually to ensure that the people who are being kicked from the channel are indeed people who should be kicked from the channel
v2: Automate by using the kick method
v3: Make less slack org specific


Outcome: Enjoy donut pairings!!

## Notice

With the change of the Slack admin backend, download of the member's activity file will have to be manual before this script can be ran.