import network
# ap config
ssid = 'ESP32'
password = '00000000'
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
ap.ifconfig(('192.168.100.1', '255.255.255.0', '192.168.100.1', '8.8.8.8'))
# ap status
print('AP Started')
print("SSID:", ssid, "Password:", password)
print(ap.ifconfig())

import utime
import time
from machine import Pin
import usocket as socket

# set gpio
led = Pin(2, Pin.OUT)

# set var
timer_running = False
timer_duration = 0
start_time = 0
led.off()

def handle_request(request):
    global timer_running, timer_duration, start_time

    print("Request received:", request)

    if '5s' in request:
        for i in range (0,5,1):
            led.on()
            if i == 4:
                led.off()
                break
            time.sleep(1)
            
    if '10s' in request:
        for i in range (0,10,1):
            led.on()
            if i == 9:
                led.off()
                break
            time.sleep(1)
    if '60s' in request:
        for i in range (0,60,1):
            led.on()
            if i == 59:
                led.off()
                break
            time.sleep(1)
    if '12m' in request:
        for i in range (0,720,1):
            led.on()
            if i == 719:
                led.off()
                break
            time.sleep(1)
    if '24m' in request:
        for i in range (0,1440,1):
            led.on()
            if i == 1439:
                led.off()
                break
            time.sleep(1)
    if '36m' in request:
        for i in range (0,2160,1):
            led.on()
            if i == 2159:
                led.off()
                break
            time.sleep(1)
    
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
            return 0  # 計時結束
        return timer_duration - elapsed_time
    return -1  # 未計時

def web_page():
    remaining_time = check_timer()
    status = "on" if led.value() == 1 else "off"
    
    html = f"""
    <html>
    <head>
        <title>ESP32 LED Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                text-align: center; 
                max-width: 400px; 
                margin: 0 auto; 
                padding: 20px;
            }}
            .timer {{ 
                font-size: 24px; 
                margin: 20px; 
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 5px;
            }}
            .btn {{ 
                display: inline-block;
                padding: 10px 20px; 
                margin: 10px; 
                font-size: 16px; 
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            input[type="number"] {{
                padding: 10px;
                margin: 10px;
                width: 200px;
            }}
        </style>
    </head>
    <body>
        <h1>LED Control Panel</h1>
        <div class="timer">
            LED Status: {status}<br>
            Time remaining: {remaining_time if remaining_time > 0 else 'None'}
        </div>
        
        <form>
            <input type="number" name="set_timer" placeholder="seconds" min="1">
            <input type="submit" value="SET" class="btn">
        </form>
        
        <div>
            <a href="?turn_on=1" class="btn">Turn on LED</a>
            <a href="?turn_off=1" class="btn">Turn off LED</a>
        </div>
        <div>
            <a href="?5s" class="btn">5s</a>
            <a href="?10s" class="btn">10s</a>
            <a href="?60s" class="btn">60s</a>
        </div>
        <div>
            <a href="?12m" class="btn">12m</a>
            <a href="?24m" class="btn">24m</a>
            <a href="?36m" class="btn">36m</a>
        </div>
    </body>
    </html>
    """
    return html

def start_server():
    addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr.bind(('0.0.0.0', 80))
    addr.listen(1)
    
    print('Web伺服器已啟動，等待連線...')
    
    while True:
        conn, client_addr = addr.accept()
#         print(f'來自 {client_addr} 的連線')
        
        try:
            request = conn.recv(1024).decode('utf-8')
            handle_request(request)
            
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
        except Exception as e:
            print('處理請求時發生錯誤:', e)
        finally:
            conn.close()

start_server()