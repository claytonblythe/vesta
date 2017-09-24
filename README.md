
## Description
Vesta is an open source home automation service that is a wrapper over the linux music player daemon (MPD). It attaches to certain local IP addresses on your home network, allowing you to trigger different events based on the activity of devices on your network. 

For example, I currently have a raspberry pi running vestaMusic.py, which is a script that monitor's my iphone IP address's activity on my home network, automatically playing random music from my Spotify playlists when I am home. After 20 minutes of network inactivity (if I leave my apartment or turn my iphone into airplane mode) the music will cut off. 

Here is an example of what the current functionality looks like, running a headless raspberry pi musicbox with Mopidy and Spotify integration.

[Alt Test](https://github.com/claytonblythe/vesta/blob/master/figures/screenshot.png)

## Next Steps
This is a simple example of how the vesta framework can be used for home automation, and I look forward to expanding it in the future. Coming up, I want to make vesta functionality separated from the events that it triggers, to allow it to be integrated into all sorts of commands like turning on lights, sending messages via Telegram or Twilio, and turning on security systems. 

If you see improvements to be made or want to assist me, feel free to open a pull request or open an issue. 

Thank you,

-Clayton Blythe <claytondblythe@gmail.com>
