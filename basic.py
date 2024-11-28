from machine import Pin
import time
led = Pin(2, Pin.OUT)
timeduration = 0
timeduration = input("Enter time duration: ")
# if type(timeduration) != int:
#     print("Please enter a number")
#     timeduration = input("Enter time duration: ")

for i in range(int(timeduration), 0, -1):
    led.on()
    print(i)
    time.sleep(1)
    # if i == timeduration:
    #     # led.off()
    #     break
    # else:
    #     continue
led.off()