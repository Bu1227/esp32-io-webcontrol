import network
import socket
import time
from machine import Pin

# wifi
ssid = 'ssid'
password = 'password'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass
print('Connection successful')
print(station.ifconfig())

# gpio
led = Pin(2, Pin.OUT)

# http
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

def web_page():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 LED Control</title>
    <script>
        function startTimer(duration) {
            var timer = duration, minutes, seconds;
            setInterval(function () {
                minutes = parseInt(timer / 60, 10);
                seconds = parseInt(timer % 60, 10);

                minutes = minutes < 10 ? "0" + minutes : minutes;
                seconds = seconds < 10 ? "0" + seconds : seconds;

                document.getElementById('time').textContent = minutes + ":" + seconds;

                if (--timer < 0) {
                    timer = duration;
                }
            }, 1000);
        }

        function startCountdown() {
            var duration = document.getElementById('duration').value;
            startTimer(duration);
            fetch('/start?duration=' + duration);
        }

        function controlLED(action) {
            fetch('/control?led=' + action);
        }
    </script>
</head>
<body>
    <h1>ESP32 LED Control</h1>
    <p>LED Timer: <input type="number" id="duration" value="10"> seconds</p>
    <button onclick="startCountdown()">Start Timer</button>
    <p>Time left: <span id="time">00:00</span></p>
    <button onclick="controlLED('on')">Turn On</button>
    <button onclick="controlLED('off')">Turn Off</button>
</body>
</html>
"""
    return html

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    if '/start' in request:
        duration = int(request.split('duration=')[1].split(' ')[0])
        led.value(1)
        time.sleep(duration)
        led.value(0)
    elif '/control?led=on' in request:
        led.value(1)
    elif '/control?led=off' in request:
        led.value(0)

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()