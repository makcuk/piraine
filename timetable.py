# -*- coding: utf-8 -*-

import datetime
import json
import RPi.GPIO as GPIO

class CronEntry:
    def __init__(self, zone, start_time, duration = 30):
        self.zone = zone
        self.start_time = start_time
        self.duration = duration

    def __repr__(self):
        return "%s start time: %s duration: %d" % (self.zone, self.start_time, self.duration)

class Zone:
    def __init__(self, zone_id, zone_desc, zone_port):
        self.zone_id = zone_id
        self.zone_desc = zone_desc
        self.zone_port = zone_port
        self.enabled = True
        self.water = False

    def run(self):
        if not self.water:
            GPIO.setup(self.zone_port, GPIO.OUT)
            GPIO.output(self.zone_port, GPIO.HIGH)
        self.water = True

    def stop(self):
        if self.water:
            GPIO.setup(self.zone_port, GPIO.OUT)
            GPIO.output(self.zone_port, GPIO.LOW)
        self.water = False

    def __repr__(self):
        return "%s" % self.zone_id


class Table(object):
    def __init__(self):

        GPIO.setmode(GPIO.BOARD)

        self.table = [
            CronEntry(Zone('zone_fence_south', u'Южный забор', 5), datetime.datetime(1,1,1,23,0), 45),
            CronEntry(Zone('zone_fence_north', 'Северный забор', 6), datetime.datetime(1,1,1,22,45), 45),
            CronEntry(Zone('zone_fence_west', 'Центральная часть', 7), datetime.datetime(1,1,1,19,25), 45),
        ]

    def next_entry(self):
        pass

    def zone_states(self):
        ret = []

        for entry in self.table:
            if entry.zone not in ret:
                ret.append(entry.zone.__dict__)
        return json.dumps(ret)

    def current(self):
        for entry in self.table:
            now = datetime.datetime.now().time()
            if now >= entry.start_time.time() and now <= (entry.start_time + datetime.timedelta(minutes = entry.duration)).time():
                entry.zone.run()
                print "Now is time to water %s" % (entry.zone.zone_desc)
            elif entry.zone.water:
                entry_zone.stop()

        return self.table
