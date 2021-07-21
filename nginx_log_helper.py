from datetime import datetime as dt
from pytz import timezone
import json


class nginx_read_log:
  def __init__(self, log_file_path, gen_file_path="./"):
    self.filepath = log_file_path
    self.f_genpath = gen_file_path
    self.list_inf = []
    self.read_file()
    self.ip_api = "http://opendata.baidu.com/api.php?resource_id=6006&oe=utf8&query="

  def deal_time(self, input_date):
    time_info = input_date
    day__ = time_info[:time_info.find("/")]#几号
    time_info = time_info[time_info.find("/")+1:]
    month__ = time_info[:time_info.find("/")]#几月
    time_info = time_info[time_info.find("/")+1:]
    year__ = time_info[:time_info.find(":")]#年份
    time_info = time_info[time_info.find(":")+1:]
    hms__ = time_info[:time_info.find(":")+6]#具体时间
    time_zone__ = time_info[time_info.find(":")+7:time_info.find(":")+12]#时区

    #debug
    #print("time_info: {}".format(time_info))
    #print("day: {}, month: {}, year: {}, hms: {}, time_zone: {}".format(day__, month__, year__, hms__, time_zone__))
    
    #键值："day" "month" "year" "hms" "time_zone"
    return {"day" : day__, "month" : month__, "year" : year__, "hms" : hms__, "time_zone" : time_zone__}
  
  def deal_hms(self, hms_input):
    hour__ = hms_input[:hms_input.index(":")]
    minute__ = hms_input[hms_input.index(":")+1:hms_input.rindex(":")]
    second__ = hms_input[hms_input.rindex(":")+1:]

    #debug
    #print("hour: {}, minute: {}, second: {}".format(hour__, minute__, second__))

    #键值：”hour“ ”minute“ "second"
    return {"hour" : hour__, "minute" : minute__, "second" : second__}

  def read_file(self):
    with open(self.filepath, "r" , encoding = 'utf-8') as f:
      for line in f.readlines(): #读行
        logs_lines = line

        ip_addr_read = logs_lines[0:logs_lines.index(" - - [")] #读取访问ip
        time_detail = logs_lines[logs_lines.find('[')+1:logs_lines.find(':')+15]

        logs_lines = logs_lines[logs_lines.index('"'):logs_lines.rindex('"')+1] #左边部分处理完成，截取右边部分
        more_detail = logs_lines.split(' "')
        for list_index, list_item in enumerate(more_detail):
          more_detail[list_index] = list_item.replace('"', "")#去掉“
        
        #debug
        #print("ip: {}, time: {}".format(ip_addr_read, time_detail))
        #print("detail: {}\n{}\n{}\n".format(more_detail[0], more_detail[1], more_detail[2]))
        
        #存储到dict
        #键值："ip" "time" "info" "url" "ua" "ext"
        dict_detail = {"ip" :  ip_addr_read, "time" : time_detail, "info" : more_detail[0], "url" : more_detail[1], "ua" : more_detail[2]}
        self.list_inf.append(dict_detail)

  #未完成部分
  '''
  def zhuan_timezone(self, tiem_input, target_tz):
    for data_item in self.list_inf:
      tzchina = timezone('Asia/Shanghai')
      time_detal_inf = self.deal_time(data_item["time"])
      hms_dict = self.deal_hms(time_detal_inf["hms"])

      date_create = dt(time_detal_inf["year"], time_detal_inf["month"], time_detal_inf["day"], hms_dict["hour"], hms_dict["minute"], hms_dict["second"], 0)
      date_create = date_create.replace()

    return time_zhuan
  '''

  def find_same_ip(self, sort=[], sort_not=[]):
    a_list = []
    all_items = []
    #把同一个ip归类
    for info_item in self.list_inf:
      if info_item["ip"] not in a_list:
        a_list.append(info_item["ip"])
    for info_item in a_list:
      list_it = []
      for i in self.list_inf:
        if i["ip"] == info_item:
          a1 = True
          a2 = True
          #排除列表
          for ii in sort_not:
            try:
              if i["info"].index(ii) >= 0:
                a1 = False
                break
            except:
              pass
          for ii in sort:
            try:
              i["info"].index(ii)
            except:
              a2 = False
              break

          if a1 == True and a2 == True:
            list_it.append(i)
      all_items.append([info_item, list_it])
    return all_items#返回如右边所示格式的列表：[["ip1","items1"], ["ip2","items2"]]
    #print(json.dumps(all_items))#debug

  def gene_date_update_json(self):
    str_date = str(dt.now().strftime('{"year" : "%Y", "month" : "%m", "day" : "%d", "hms" : "%H:%M:%S"'))
    str_date += ', "api" : "' + self.ip_api + '"}'
    with open(self.f_genpath + "update_date.json", 'w', encoding = 'utf-8') as fil:
      fil.write(str_date)

  def gene_json(self, select_ = 0, file_n = "data.json", sort=[], sort_not=[]):
    all_items_ = self.find_same_ip(sort, sort_not)
    #print(all_items_)#debug
    ret_list = []

    for ind, ite in enumerate(all_items_):
      info_item = []
      info_item.extend(ite)
      
      if True:
        if select_ == 0: #不显示ip
          info_item[0] = ( "ID"+str(ind+1) )
        for it in info_item[1]:
          time_list = self.deal_time(it["time"])
          if select_ == 0: #不显示ip
            it["ip"] = ( "ID"+str(ind+1) )
          it["time_detail"] = time_list#存入新的键

      ret_list.append(info_item)

      
    with open(self.f_genpath + file_n, 'w', encoding = 'utf-8') as fil:
      fil.write(json.dumps(ret_list))

    #print(json.dumps(ret_list))#debug
    

if __name__ == '__main__':
  test = nginx_read_log("./access.log", "./templates/")
  test.gene_json(0, file_n = "data.json")
  test.gene_json(0, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
  test.gene_date_update_json()