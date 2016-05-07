#!/usr/bin/python
import re


def parser(record_file_name="AP_signal.txt"):
    record = open(record_file_name, 'r')

    ap_dic = {}

    position = ""
    for line in record:
        if line[:3] == "***":
            position = line.split()[1]
        elif "SSID BSSID" in line:
            continue
        elif line == "":
            continue
        else:
            data = line.split()
            result = re.search(r'([0-9a-f]{2}:){5}[0-9a-f]{2}', line)
            if result is None:
                # print line
                # print "cannot find mac address"
                continue
            MAC_addr = result.group()
            mac_pos = -1
            for i in range(0, len(data)):
                if data[i] == MAC_addr:
                    mac_pos = i
                    break
            SSID = ' '.join(data[0:mac_pos])
            RSSI = data[mac_pos + 1]
            CHANNEL = data[mac_pos + 2]
            HT = data[mac_pos + 3]
            CC = data[mac_pos + 4]
            SECURITY = data[mac_pos + 5]
            if MAC_addr not in ap_dic:
                ap_dic[MAC_addr] = {}
                ap_dic[MAC_addr]["vector"] = []
                ap_dic[MAC_addr]["SSID"] = SSID
            ap_dic[MAC_addr]["vector"].append({"position": position, "RSSI": RSSI, "CHANNEL": CHANNEL,
                                               "HT": HT, "CC": CC, "SECURITY": SECURITY})
    record.close()

    output = []
    for mac, ap_record in ap_dic.iteritems():
        for pos_info in ap_record["vector"]:
            output.append("%s %10s %10s %20s" % (mac, pos_info["position"], pos_info["RSSI"],
                                                 ap_record["SSID"]))
    return output

if __name__ == "__main__":
    output = parser()
    for line in output:
        print line
