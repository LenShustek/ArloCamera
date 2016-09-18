The Netgear Arlo is a neat battery-powered wireless camera that you can
just stick on a wall or shelf anywhere. See www.arlo.com.

Unfortunately the only way to turn motion sensing on and off is either 
by preset schedule (which doesn't work for us) or by clicking a bunch 
of menus on their web interface (which is a pain). I wanted a way to
turn on motion sensing by just pushing a button when I leave the house.

So I took a Raspberry Pi computer, added a switch and lights, and 
programmed it to enable or disable the Arlo camera motion sensing. 
You push the switch either up or down, and it logs into the Arlo 
website and changes the mode. It takes about 10 seconds.

The file "instructions.txt" is a description of how to build this.
I would say it is a "medium hard" do-it-yourself project.

-- Len Shustek, 11 Aug 2015; updated 14 Sep 2016 to use Jeffrey Walter's 
   great Arlo HTTP Python library instead of doing browser mouse clicks
