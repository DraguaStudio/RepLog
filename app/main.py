import network
from machine import Pin
from utime import sleep, sleep_ms, ticks_ms, ticks_diff

def run_loading(n: int, msg: str, delay: int = 400) -> None:
    for i in range(1, n):
        print("." * i)
        sleep_ms(delay)

    print(msg)


def connect_to_wifi(ssid: str, password: str) -> None:
    print("Connecting to WiFi Network Name: ", ssid)
    lan = network.WLAN(network.STA_IF)
    lan.active(True)

    start: int = ticks_ms() # start a millisecond counter

    if not lan.isconnected():
        lan.connect(ssid, password)
        print("Waiting for connection ...")
        counter = 0
        while not lan.isconnected():
            sleep(1)
            print(counter, '.', sep='', end='', )
            counter += 1

    delta: int = ticks_diff(ticks_ms(), start)
    print(f"Connect Time: {delta} milliseconds")
    print(f"IP Address: {lan.ifconfig()[0]}")


def main() -> None:
    print("Running ...")

    run_loading(5, "Connecting to wifi ...")

    connect_to_wifi("", "")                     # Write your wifi SSID and PASSWORD

    run_loading(5, "Hardware setup ...")

    LED = Pin("LED", Pin.OUT)
    MOVE_SENSOR_INPUT = Pin(16, Pin.IN, Pin.PULL_DOWN)
    LED.value(0)

    is_active = False
    count = 0

    run_loading(5, "Start main program ...")

    # Show that program is ready
    for _ in range(5):
        LED.toggle()
        sleep_ms(150)

    print(f"Count: {count}")

    while True:
        if MOVE_SENSOR_INPUT.value() == 0:      # In sensor
            is_active = True
            LED.value(1)
            sleep_ms(100)
        else:                                   # Out of sensor
            if is_active:
                count += 1
                is_active = False
                print(f"Count: {count}")

            LED.value(0)
            sleep_ms(100)


if __name__ == "__main__":
    main()
