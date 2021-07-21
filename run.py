from nginx_log_helper import nginx_read_log
import time

sleep = 30 #分钟

last_time = time.time()
while True:
    now_ti = time.time()
    if now_ti - last_time > (sleep/60):
        log = nginx_read_log("./access.log", "./")
        log.gene_json(0, file_n = "data.json")
        log.gene_json(0, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
        log.gene_date_update_json()
        print("Finished...")
        last_time = time.time()
    else:
        time.sleep(0.00001)