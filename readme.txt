The Netgear Arlo is a neat battery-powered wireless camera that you can
just stick on a wall or shelf anywhere. See www.arlo.com.

Unfortunately the only way to turn motion sensing on and off is either 
by preset schedule (which doesn't work for us) or by clicking a bunch 
of menus on their web interface (which is a pain). I wanted a way to
turn on motion sensing by just pushing a button when I leave the house.
Even more importantly, I wanted a way to have it monitor the state of
our ancient security system, so that when the security system is armed,
the cameras are too, and vice versa.

So I took a Raspberry Pi computer, added a switch and lights, and 
programmed it to enable or disable the Arlo camera motion sensing. You 
push the switch either up or down, and it uses the Arlo website to 
change the mode. It takes about 5 seconds. The contact-closure output 
of the security system is wired to a Raspberry Pi input and does the 
same thing. 

There have been three iterations of the software:

- Version 1 in 2015 used simulated mouse motion in a browser to log on to
my Arlo account and arm or disarm the cameras. Not a robust solution!

- Version 2 in 2016 used Jeffrey Walter's great Arlo HTTP Python library
to directly access the Arlo API. Much nicer, and I ran that for 6 years,
until Arlo's use of 2-factor authentication broke it.

- Version 3 in 2022 instead uses the IFTTT ("If This Then That") service, 
www.ifttt.com, which has an officially-sanctioned link to Arlo as a third-
party service. It is fast, free, and works quite well.
  
The file "instructions.txt" is a description of how to build this.
I would say it is a "medium hard" do-it-yourself project.

-- Len Shustek, 11 Aug 2015, 14 Sep 2016, 18 Mar 2022