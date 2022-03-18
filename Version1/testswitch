#!/bin/bash

# script to test the Arlo camera switch and lights
# L. Shustek, 11 Aug 2015
# L. Shustek, 17 Aug 2015; add green LED

# GPIO9 is input with pullup: "up" momentary toggle switch leg
echo 9 | sudo tee /sys/class/gpio/export > /dev/null
echo "in" | sudo tee /sys/class/gpio/gpio9/direction > /dev/null
echo "high" | sudo tee /sys/class/gpio/gpio9/direction > /dev/null

#GPIO10 is input with pullup: "down" momentary toggle switch leg
echo 10 | sudo tee /sys/class/gpio/export > /dev/null
echo "in" | sudo tee /sys/class/gpio/gpio10/direction > /dev/null
echo "high" | sudo tee /sys/class/gpio/gpio10/direction > /dev/null

#GPIO11 is output: a red LED through a 680 ohm resistor to ground
echo 11 | sudo tee /sys/class/gpio/export > /dev/null
echo "out" | sudo tee /sys/class/gpio/gpio11/direction > /dev/null

#GPIO22 is output: a green LED through a 1K ohm resistor to ground
echo 22 | sudo tee /sys/class/gpio/export > /dev/null
echo "out" | sudo tee /sys/class/gpio/gpio22/direction > /dev/null

echo push the switch up or down
while true; do
 read val < /sys/class/gpio/gpio9/value
 if (( val == 0 )); then
  echo switch up
  echo 1 > /sys/class/gpio/gpio11/value  
  echo 0 > /sys/class/gpio/gpio22/value
  sleep 1
  fi
read val < /sys/class/gpio/gpio10/value
 if (( val == 0 )); then
  echo switch down
  echo 0 > /sys/class/gpio/gpio11/value  
  echo 1 > /sys/class/gpio/gpio22/value
  sleep 1
  fi
done
