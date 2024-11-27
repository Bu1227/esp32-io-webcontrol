import network
import machine
import utime
from microWebSrv import MicroWebSrv

# wifi
ssid = "SSID"
password = "password"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# set pin
led_pin = machine.Pin(2, machine.Pin.OUT)

# set webserver
root_dir = "/"  # 網頁檔案路徑
port = 80     # 伺服器端口
mws = MicroWebSrv(root_dir, port)

# set timer
timer_running = False
timer_duration = 0

# web
def handle_root(httpClient, httpResponse):
    # 顯示設定時間和倒數計時
    global timer_running, timer_duration
    html = f"""
    <html>
    <head>
        <title>LED控制</title>
    </head>
    <body>
        <form method="post" action="/set_timer">
            設定亮燈時間(秒): <input type="number" name="duration">
            <input type="submit" value="設定">
        </form>
        <p>倒數計時: <span id="timer"></span> 秒</p>
        <button onclick="toggleLed('on')">開燈</button>
        <button onclick="toggleLed('off')">關燈</button>
        <script>
            function toggleLed(state) {
                fetch('/toggle_led?state=' + state);
            }
            // JavaScript用於更新倒數計時顯示
            // ...
        </script>
    </body>
    </html>
    """
    httpResponse.send(200, "text/html", html)

# timer
def handle_set_timer(httpClient, httpResponse):
    global timer_running, timer_duration
    duration = int(httpClient.args['duration'][0])
    timer_duration = duration
    timer_running = True
    # 開始倒數計時
    # ...
    httpResponse.send(200, "text/html", "設定成功")

# LED
def handle_toggle_led(httpClient, httpResponse):
    global led_pin
    state = httpClient.args['state'][0]
    if state == 'on':
        led_pin.value(1)
    else:
        led_pin.value(0)
    httpResponse.send(200, "text/html", "LED狀態已更新")

# route
mws.GET("/", handle_root)
mws.POST("/set_timer", handle_set_timer)
mws.GET("/toggle_led", handle_toggle_led)

# start webserver
mws.start()