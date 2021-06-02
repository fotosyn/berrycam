# rebuilding/testing (from the berrycam_0.0-1_armhf folder in berrycam repo [on raspberrypi])
1. sudo rm -f berrycam_0.0-1_armhf.deb  # remove the old deb package
2. # change the DEBIAN/control contents (version and info) as necessary
3. sudo dpkg-deb --build --root-owner-group berrycam_0.0-1_armhf
4. sudo apt install ./berrycam_0.0-1_armhf.deb -y
5. sudo systemctl status berryCam  # should be running