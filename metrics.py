import psutil, time

while True:
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    net = psutil.net_io_counters()
    print(f"CPU: {cpu}% | Memory: {mem}% | Disk: {disk}%")
    print(f"Network sent: {net.bytes_sent} | received: {net.bytes_recv}")
    time.sleep(2)

