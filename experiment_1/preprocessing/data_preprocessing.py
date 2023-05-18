import requests
import xml.etree.ElementTree as et
import pyshark
import csv
import nest_asyncio
import sys
import os
import time

nest_asyncio.apply()

start_time = time.time()

for file in os.listdir():
  csv_file = ''
  if file.endswith(".pcap"):
    cap = pyshark.FileCapture(file)
    print(f'[!] File {file} was loaded.')
    print(f'[!] Processing packets...')
    headings = ["frame.time","frame.len","frame.protocols","frame.time_delta","ip.src","ip.dst","tcp.window_size"]
    packet_list = []
    packet_list.append(headings)
    i = 0
    for packet in cap:
      temp = []
      temp.append(str(packet.frame_info._all_fields["frame.time"]) )#0
      temp.append(str(packet.frame_info._all_fields["frame.len"])) #1
      temp.append(str(packet.frame_info._all_fields["frame.protocols"])) #2
      temp.append(str(packet.frame_info._all_fields['frame.time_delta']))#6
      if hasattr(packet, 'ip'):
        temp.append(str(packet.ip._all_fields['ip.src']))#3
        temp.append(str(packet.ip._all_fields['ip.dst']))#4
      else:
        temp.extend(["0","0"])
      if hasattr(packet, 'tcp'):
        temp.append(str(packet.tcp._all_fields['tcp.window_size']))#5
      else:
        temp.extend(["0"])
      packet_list.append(temp)
      i = i + 1
      sys.stdout.flush()
      now = time.time()
      duration = now - start_time
      time_now = time.strftime("%H:%M:%S", time.gmtime(duration))
      print(str(i) + ' packets extracted / elapsed time: ' + str(time_now), end = "\r")

    csv_file = file + '.csv'
    with open(csv_file, 'w') as writeFile:
      writer = csv.writer(writeFile)
      writer.writerows(packet_list)

    now = time.time()
    duration = now - start_time
    time_now = time.strftime("%H:%M:%S", time.gmtime(duration))
    print(f'[+] File {csv_file} was created. / elapsed time: {time_now}')