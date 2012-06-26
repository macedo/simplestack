import unittest
import random
import ConfigParser
from simplestack.hypervisors import xen
from simplestack.tests.hypervisors.base_test_case import HypervisorBaseTest


class XenTest(unittest.TestCase, HypervisorBaseTest):
    @classmethod
    def setUpClass(clazz):
        conf = ConfigParser.ConfigParser()
        conf.read("test.cfg")
        clazz.stack = xen.Stack({"api_server": conf.get("xen", "api_server"), "username": conf.get("xen", "username"), "password": conf.get("xen", "password")})
        clazz.vm_name = "TestVM:%f" % random.random()
        main_vm_ref = clazz.stack.connection.xenapi.VM.get_by_uuid("6562aace-6bae-4e58-bf62-c4ec62a1e6c6")
        vm_ref = clazz.stack.connection.xenapi.VM.clone(main_vm_ref, clazz.vm_name)
        clazz.vm = clazz.stack.connection.xenapi.VM.get_record(vm_ref)

    @classmethod
    def tearDownClass(clazz):
        clazz._stopVmClass()
        clazz.stack.guest_delete(clazz.vm['uuid'])

    @classmethod
    def _stopVmClass(clazz):
        ref = clazz.stack.connection.xenapi.VM.get_by_uuid(clazz.vm['uuid'])
        try:
            clazz.stack.connection.xenapi.VM.resume(ref)
        except:
            pass
        try:
            clazz.stack.connection.xenapi.VM.start(ref, False, True)
        except:
            pass
        try:
            clazz.stack.connection.xenapi.VM.hard_shutdown(ref)
        except:
            pass

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm
        ref = self.stack.connection.xenapi.VM.get_by_uuid(self.vm['uuid'])
        try:
            self.stack.connection.xenapi.VM.start(ref, False, True)
        except:
            pass

    def _get_vm_id(self):
        return self.vm['uuid']

    def _get_nw_interface_id(self):
        return "0"

    def _stop_vm(self):
        self.__class__._stopVmClass()

    def _media_name(self):
        return "systemrescuecd-x86-2.7.0.iso"

    def test_guest_suspend(self):
        pass

    def test_guest_resume(self):
        pass
