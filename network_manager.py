import network
import time

class NetworkManager:
    CONNECT_SLEEP_DUR = 1

    def __init__(self, ssid, password, timeout=1, retries=5):
        self.wlan = network.WLAN(network.STA_IF)
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.retries = retries

    def connect(self):
        print("Wifi Connect to ", self.ssid)
        retries = 0
        conn_timer = 0

        self.wlan.active(True)

        while not self.wlan.isconnected() and retries < self.retries:
            print("Connect Attempt ", retries)
            retries += 1
            conn_timer = 0
            self.wlan.connect(self.ssid, self.password)

            status = self.wlan.status()
            while status == network.STAT_CONNECTING and conn_timer < self.timeout:
                print("Status ", status, " after ", conn_timer, " seconds")
                conn_timer += self.CONNECT_SLEEP_DUR
                time.sleep(self.CONNECT_SLEEP_DUR)
                status = self.wlan.status()

            if status == network.STAT_WRONG_PASSWORD:
                break

        print("Wifi Connect Done. Final Status: ", self.wlan.status())
        return self.wlan.status()
    
    def is_connected(self):
        return self.wlan.isconnected()