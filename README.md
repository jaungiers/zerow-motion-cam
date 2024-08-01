# zerow-motion-cam

Simple motion detection code for use with Raspberry Pi ZeroW and PiCamera.

Motion calculation using absolute percentage difference between two frames. If motion is detected, camera starts recording at normal video frame rate into individual video file until the motion has stopped. Individual motion videos are datetime tagged.

To make the script launchable on startup copy the configuration `zerow-motion-cam.service` into  `/etc/systemd/system/zerow-motion-cam.service` with the correct username then enable with:

* `sudo systemctl daemon-reload`
* `sudo systemctl enable zerow-motion-cam.service`
* `sudo systemctl start zerow-motion-cam.service`
