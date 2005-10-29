#!/usr/bin/env python
import sys
import os

builddir = os.environ["DBUS_TOP_BUILDDIR"]
pydir = builddir + "/python"

sys.path.insert(0, pydir)
sys.path.insert(0, pydir + '/.libs')

import dbus

if not dbus.__file__.startswith(pydir):
    raise Exception("DBus modules are not being picked up from the package")

import dbus.service
import dbus.glib
import gobject
import random

class TestObject(dbus.service.Object):
    def __init__(self, bus_name, object_path="/org/freedesktop/DBus/TestSuitePythonObject"):
        dbus.service.Object.__init__(self, bus_name, object_path)

    """ Echo whatever is sent
    """
    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface")
    def Echo(self, arg):
        return arg

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface")
    def GetComplexArray(self):
        ret = []
        for i in range(0,100):
            ret.append((random.randint(0,100), random.randint(0,100), str(random.randint(0,100))))

        return dbus.Array(ret, signature="(uus)")

    def returnValue(self, test):
        if test == 0:
            return ""
        elif test == 1:
            return "",""
        elif test == 2:
            return "","",""
        elif test == 3:
            return []
        elif test == 4:
            return {}
        elif test == 5:
            return ["",""]
        elif test == 6:
            return ["","",""]

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface", in_signature='u', out_signature='s')
    def ReturnOneString(self, test):
        return self.returnValue(test)

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface", in_signature='u', out_signature='ss')
    def ReturnTwoStrings(self, test):
        return self.returnValue(test)

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface", in_signature='u', out_signature='(ss)')
    def ReturnStruct(self, test):
        return self.returnValue(test)

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface", in_signature='u', out_signature='as')
    def ReturnArray(self, test):
        return self.returnValue(test)

    @dbus.service.method("org.freedesktop.DBus.TestSuiteInterface", in_signature='u', out_signature='a{ss}')
    def ReturnDict(self, test):
        return self.returnValue(test)

session_bus = dbus.SessionBus()
name = dbus.service.BusName("org.freedesktop.DBus.TestSuitePythonService", bus=session_bus)
object = TestObject(name)
loop = gobject.MainLoop()
loop.run()
