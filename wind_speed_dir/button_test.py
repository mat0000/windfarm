from gpiozero import Button

wind_speed_sensor = Button(24)
wind_count = 0

def spin():
    global wind_count
    wind_count = wind_count + 1
    print("spin" + str(wind_count))

while True:
    wind_speed_sensor.when_pressed = spin