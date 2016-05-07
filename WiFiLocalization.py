#!/usr/bin/python
import copy
from Tkinter import *
import tkFileDialog
import tkFont
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import AP_signal_parser
import math
import operator
from collections import OrderedDict

# map image
PIC_PATH = "Courant-library-floorplan.jpg"
# map signal data file
COURANT_SIGNAL_FILE = "AP_signal.txt"
# map mac address to SSID dictionary
SSID_DICT = AP_signal_parser.get_SSID_dict(COURANT_SIGNAL_FILE)

DISTANCE_THRESHOLD = 100

FONT_PATH = os.environ.get("FONT_PATH", "/Library/Fonts/Times New Roman.ttf")

# map signal data point
MAP_DATA_COR = []
MAP_DATA_COR.append((921, 436))
MAP_DATA_COR.append((751, 433))
MAP_DATA_COR.append((621, 438))
MAP_DATA_COR.append((519, 433))
MAP_DATA_COR.append((335, 372))
MAP_DATA_COR.append((159, 376))
MAP_DATA_COR.append((103, 424))
MAP_DATA_COR.append((106, 265))
MAP_DATA_COR.append((109, 103))
MAP_DATA_COR.append((223, 181))
MAP_DATA_COR.append((248, 59))
MAP_DATA_COR.append((336, 184))
MAP_DATA_COR.append((338, 271))
MAP_DATA_COR.append((490, 181))
MAP_DATA_COR.append((708, 175))
MAP_DATA_COR.append((856, 173))
MAP_DATA_COR.append((756, 65))
MAP_DATA_COR.append((938, 62))
MAP_DATA_COR.append((917, 245))
MAP_DATA_COR.append((862, 364))


class SignalDataDialog:
    """
    Predicted Signal Data Dialog
    """
    def __init__(self, parent, signal):
        top = self.top = Toplevel(parent)
        title_font = tkFont.Font(weight=tkFont.BOLD)
        Label(top, text="Predicted WiFi Signal", font=title_font).pack()

        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)

        listbox = Listbox(top, yscrollcommand=scrollbar.set, borderwidth=0, height=20, width=50)

        # sort in ascending ordier
        sorted_x = sorted(signal.items(), key=operator.itemgetter(1))
        sorted_x.reverse()
        signal = OrderedDict(sorted_x)
        for mac, rssi in signal.iteritems():
            listbox.insert(END, "%20s %20s: %5d" % (SSID_DICT[mac], mac, rssi))
        listbox.pack(side=LEFT, fill=BOTH)

        scrollbar.config(command=listbox.yview)


class WiFiLocalization(Frame):
    """
    WiFi Localization Application GUI
    """
    @staticmethod
    def calcTargetLocation(map_data, target_data):
        """
        Calculate target position by signal strength
        measured at this position
        :param map_data: parsed map signal data from AP_signal_parser.parser()
        :param target_data: parsed target position signal data from AP_signal_parser.parser()
        :return: target coordinate x, y
        """
        target_avg_rssi = 0

        for mac, data in target_data[target_data.keys()[0]].iteritems():
            target_avg_rssi += data["RSSI"]
        target_avg_rssi = float(target_avg_rssi) / len(target_data[target_data.keys()[0]])

        target_strong_ap_list = []
        for mac, data in target_data[target_data.keys()[0]].iteritems():
            if data["RSSI"] > target_avg_rssi:
                target_strong_ap_list.append(mac)

        possible_location_dic = {}
        for location, ap_data in map_data.iteritems():
            match = True
            for target_strong_ap in target_strong_ap_list:
                if target_strong_ap not in ap_data:
                    match = False
                    break
            if match:
                possible_location_dic[location] = 0

        if len(possible_location_dic) == 0:
            print >>sys.stderr, "no possible location, maybe target is too far away"
            return 0, 0

        # calculate distances to all possible location
        for possible_location in possible_location_dic:
            sum = 0
            for mac, data in target_data[target_data.keys()[0]].iteritems():
                if mac in map_data[possible_location]:
                    abs_rssi = abs(map_data[possible_location][mac]["RSSI"] - data["RSSI"])
                    sum += abs_rssi * abs_rssi
            possible_location_dic[possible_location] = math.sqrt(sum)
            print "Possible %s location distance: %f" % (possible_location, possible_location_dic[possible_location])

        x_denominator = 0
        for possible_location, distance in possible_location_dic.iteritems():
            x_denominator += 1 / distance
        x_numerator = 0
        for possible_location, distance in possible_location_dic.iteritems():
            x_numerator += MAP_DATA_COR[int(possible_location)][0] / distance

        y_denominator = 0
        for possible_location, distance in possible_location_dic.iteritems():
            y_denominator += 1 / distance
        y_numerator = 0
        for possible_location, distance in possible_location_dic.iteritems():
            y_numerator += MAP_DATA_COR[int(possible_location)][1] / distance

        target_x = x_numerator / x_denominator
        target_y = y_numerator / y_denominator
        print "Target coordinate: %f, %f" % (target_x, target_y)

        return target_x, target_y

    @staticmethod
    def calcTargetSignal(x, y, map_data):
        """
        Calculate predicted AP signal at target position
        :param x: target position coordinate
        :param y: target position coordinate
        :param map_data: parsed map signal data from AP_signal_parser.parser()
        :return: possible AP signal mac address and RSSI
        """
        target_signal_dict = {}
        distances = []
        candidate_position_list = []
        min_distance = sys.float_info.max
        for i in range(0, len(MAP_DATA_COR)):
            distance = math.sqrt((MAP_DATA_COR[i][0]-x)**2 + (MAP_DATA_COR[i][1]-y)**2)
            distances.append(distance)

            if distance < min_distance:
                min_distance = distance

        # find all neighbor point (distance less than threshold)
        for i in range(0, len(distances)):
            if distances[i] - min_distance < DISTANCE_THRESHOLD:
                candidate_position_list.append(i)
        if len(candidate_position_list) == 0:
            print >>sys.stderr, "No candidate position, target point is too far away from map data point"
            return target_signal_dict

        candidate_distance_sum = 0
        all_signal_set = set()
        for candidate in candidate_position_list:
            print "Distance to point %d: %f" % (candidate+1, distances[candidate])
            candidate_distance_sum += distances[candidate]
            for mac in map_data[str(candidate+1)]:
                all_signal_set.add(mac)

        for mac in all_signal_set:
            target_signal_dict[mac] = 0
            for candidate in candidate_position_list:
                if mac in map_data[str(candidate+1)]:
                    rssi = map_data[str(candidate+1)][mac]["RSSI"]
                else:
                    rssi = -100
                target_signal_dict[mac] += rssi * distances[candidate]/candidate_distance_sum

        return target_signal_dict

    def localizeTarget(self):
        self.file_opt = {}
        self.file_opt['initialdir'] = os.getcwd()
        self.file_opt['parent'] = root
        self.file_opt['title'] = 'Open target AP signal file'
        filename = tkFileDialog.askopenfilename(**self.file_opt)

        target_data = AP_signal_parser.parser(filename)

        target_x, target_y = self.calcTargetLocation(self.courant_data, target_data)

        self.drawPoint(target_x, target_y)

    def drawOriMap(self):
        """
        Draw map signal data point on map.
        New point is drawed on this map.
        """
        draw = ImageDraw.Draw(self.oriCourantLibMap)
        font = ImageFont.truetype("Times New Roman.ttf", 30)
        for i in range(0, len(MAP_DATA_COR)):
            draw.text(MAP_DATA_COR[i], str(i+1), fill="red", font=font)
        del draw

    def drawPoint(self, x, y):
        self.courantLibMap = copy.deepcopy(self.oriCourantLibMap)
        draw = ImageDraw.Draw(self.courantLibMap)
        new_cor = (x, y)
        font = ImageFont.truetype("Times New Roman.ttf", 30)
        r = 2
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(0, 255, 0, 0))
        draw.text(new_cor, "target", fill=(0, 255, 0, 0), font=font)
        del draw

        # update image
        self.img = ImageTk.PhotoImage(self.courantLibMap)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def createWidgets(self):
        self.localizeButton = Button(self)
        self.localizeButton["text"] = "Localize",
        self.localizeButton["command"] = self.localizeTarget
        self.localizeButton.pack({"side": "top"})

        self.frame = Frame(self, bd=2, relief=SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frame, bd=0, height=547, width=1029)
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)

        self.frame.pack(fill=BOTH, expand=1)

        self.img = ImageTk.PhotoImage(self.oriCourantLibMap)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        def click_handler(event):
            print "Click point:", (event.x, event.y)
            self.drawPoint(event.x, event.y)
            signal = self.calcTargetSignal(event.x, event.y, self.courant_data)

            d = SignalDataDialog(self, signal)
            self.wait_window(d.top)

        # mouse click event
        self.canvas.bind("<Button 1>", click_handler)

    def __init__(self, courantSignalFile, master=None):
        self.courant_data = AP_signal_parser.parser(courantSignalFile)
        master.title("WiFi Localization")
        Frame.__init__(self, master)
        self.pack()
        self.oriCourantLibMap = Image.open(PIC_PATH)
        self.drawOriMap()
        self.courantLibMap = copy.deepcopy(self.oriCourantLibMap)
        self.createWidgets()


if __name__ == "__main__":
    root = Tk()
    app = WiFiLocalization(COURANT_SIGNAL_FILE, master=root)
    app.mainloop()
