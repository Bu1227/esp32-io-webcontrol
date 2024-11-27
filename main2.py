import network
import utime
import machine
import usocket as socket

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    while not station.isconnected():
        utime.sleep(1)
    
    print('Network Configuration:', station.ifconfig())
    return station

# gpio
led = machine.Pin(2, machine.Pin.OUT)  # onboard LED

# set vars
timer_running = False
timer_duration = 0
start_time = 0

def handle_request(request):
    global timer_running, timer_duration, start_time
    if 'set_timer=' in request:
        # set timer
        duration = int(request.split('set_timer=')[1].split(' ')[0])
        timer_duration = duration
        timer_running = True
        start_time = utime.time()
        led.on()
    if 'turn_on' in request:
        led.on()
        timer_running = False
    if 'turn_off' in request:
        led.off()
        timer_running = False

def check_timer():
    global timer_running, timer_duration, start_time
    if timer_running:
        elapsed_time = utime.time() - start_time
        if elapsed_time >= timer_duration:
            led.off()
            timer_running = False
            return 0
        return timer_duration - elapsed_time
    return -1

def web_page():
    remaining_time = check_timer()
    status = "開" if led.value() == 1 else "關"
    
    html = f"""
    <html>
    <head>
        <title>ESP32 LED 控制器</title>
        <style>
            body {{ font-family: Arial; text-align: center; }}
            .timer {{ font-size: 24px; margin: 20px; }}
            .btn {{ 
                padding: 10px 20px; 
                margin: 10px; 
                font-size: 16px; 
            }}
        </style>
    </head>
    <body>
        <h1>LED 控制台</h1>
        <div class="timer">
            LED狀態: {status}<br>
            剩餘時間: {remaining_time if remaining_time > 0 else '無計時'}
        </div>
        
        <form>
            <input type="number" name="set_timer" placeholder="設定秒數" min="1">
            <input type="submit" value="設定計時器" class="btn">
        </form>
        
        <div>
            <a href="?turn_on=1" class="btn">開啟LED</a>
            <a href="?turn_off=1" class="btn">關閉LED</a>
        </div>
    </body>
    </html>
    """
    return html

def start_server():
    addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr.bind(('0.0.0.0', 80))
    addr.listen(1)
    print('Web server startes, waiting for connections...')
    
    while True:
        conn, addr = addr.accept()
        print(f'來自 {addr} 的連線')
        request = conn.recv(1024).decode('utf-8')
        handle_request(request)
        
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

# # 連接WiFi
# connect_wifi('您的WiFi名稱', '您的WiFi密碼')

# 啟動伺服器
start_server()