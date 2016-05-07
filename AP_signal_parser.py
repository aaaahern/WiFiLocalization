#!/usr/bin/python
import re
from collections import OrderedDict


def get_SSID_dict(file_name):
    """
    Get mac address to SSID dictionary
    :param file_name: map signal data file
    :return: mac address to SSID dictionary
    """
    SSID_dict = {}
    record = open(file_name, 'r')

    for line in record:
        if line[:3] == "***":
            continue
        elif "SSID BSSID" in line:
            continue
        elif line == "":
            continue
        else:
            data = line.split()
            result = re.search(r'([0-9a-f]{2}:){5}[0-9a-f]{2}', line)
            if result is None:
                continue
            MAC_addr = result.group()
            mac_pos = -1
            for i in range(0, len(data)):
                if data[i] == MAC_addr:
                    mac_pos = i
                    break
            SSID = ' '.join(data[0:mac_pos])

            if MAC_addr not in SSID_dict:
                SSID_dict[MAC_addr] = SSID
    record.close()
    return SSID_dict


def parser(record_file_name):
    """
    Parse signal data from AP_signal.sh script
    :param record_file_name:
    :return:
    """
    record = open(record_file_name, 'r')

    ap_dic = OrderedDict()

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
            # CHANNEL = data[mac_pos + 2]
            # HT = data[mac_pos + 3]
            # CC = data[mac_pos + 4]
            # SECURITY = data[mac_pos + 5]
            if position not in ap_dic:
                ap_dic[position] = {}
            ap_dic[position][MAC_addr] = {}
            ap_dic[position][MAC_addr]["SSID"] = SSID
            ap_dic[position][MAC_addr]["RSSI"] = int(RSSI)
    record.close()

    return ap_dic

if __name__ == "__main__":
    ap_dic = parser("AP_signal.txt")
    for pos, ap_record in ap_dic.iteritems():
        for mac, info in ap_record.iteritems():
            print "%s %10s %10s %20s" % (pos, mac, info["RSSI"], info["SSID"])
