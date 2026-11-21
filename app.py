import psutil
from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

cpu_g = Gauge("server_cpu_percent", "CPU usage percent")
mem_g = Gauge("server_memory_percent", "Memory usage percent")
disk_g = Gauge("server_disk_percent", "Disk usage percent")
sent_g = Gauge("server_network_sent_bytes", "Network bytes sent")
recv_g = Gauge("server_network_received_bytes", "Network bytes received")
proc_cpu = Gauge("server_top_process_cpu_percent", "CPU percent of top processes", ["name", "pid"])

@app.get("/metrics")
def metrics():
    cpu_g.set(psutil.cpu_percent(interval=0.5))
    mem_g.set(psutil.virtual_memory().percent)
    disk_g.set(psutil.disk_usage("/").percent)
    net = psutil.net_io_counters()
    sent_g.set(net.bytes_sent)
    recv_g.set(net.bytes_recv)

    proc_cpu.clear()
    procs = [p.info for p in psutil.process_iter(["pid", "name", "cpu_percent"])]
    top = sorted(procs, key=lambda x: x["cpu_percent"] or 0, reverse=True)[:5]
    for p in top:
        proc_cpu.labels(name=p["name"] or "unknown", pid=str(p["pid"])).set(p["cpu_percent"] or 0)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
