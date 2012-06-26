import random


class HypervisorBaseTest(object):

    def test_pool_info(self):
        pool = self.stack.pool_info()
        self.assertNotEqual(pool.get("total_memory"), None)
        self.assertNotEqual(pool.get("used_memory"), None)
        self.assertNotEqual(pool.get("master"), None)

    def test_guest_info(self):
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["id"], self._get_vm_id())
        self.assertFalse(guest["tools_up_to_date"])

    def test_guest_start(self):
        self._stop_vm()
        self.stack.guest_start(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_force_reboot(self):
        force = True
        self.stack.guest_reboot(self._get_vm_id(), force)
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_reboot(self):
        # The created vm should have the correct tool for this method
        return

        self.stack.guest_reboot(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_shutdown(self):
        force = True
        self.stack.guest_shutdown(self._get_vm_id(), force)
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STOPPED")

    def test_guest_suspend(self):
        self.stack.guest_suspend(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "PAUSED")

    def test_guest_resume(self):
        self.stack.guest_suspend(self._get_vm_id())
        self.stack.guest_resume(self._get_vm_id())
        guest = self.stack.guest_info(self._get_vm_id())
        self.assertEqual(guest["state"], "STARTED")

    def test_guest_update(self):
        guest_data = {"memory": 128, "cpus": 2, "name": "vm%f" % random.random(), "hdd": 50}
        self.stack.guest_shutdown(self._get_vm_id(), True)
        guest = self.stack.guest_update(self._get_vm_id(), guest_data)
        self.assertEqual(guest["memory"], guest_data["memory"])
        self.assertEqual(guest["cpus"], guest_data["cpus"])
        self.assertEqual(guest["name"], guest_data["name"])
        self.assertEqual(guest["hdd"], guest_data["hdd"])

    def test_media_unmount(self):
        self.stack.media_mount(self._get_vm_id(), {"name": None})
        media = self.stack.media_info(self._get_vm_id())
        self.assertEqual(media["name"], None)

    def test_media_mount(self):
        self.stack.media_mount(self._get_vm_id(), {"name": self._media_name()})
        media = self.stack.media_info(self._get_vm_id())
        self.assertEqual(media["name"], self._media_name())

    def test_network_interface_list(self):
        nw_interfaces = self.stack.network_interface_list(self._get_vm_id())
        self.assertEqual(len(nw_interfaces), 1)

    def test_network_interface_info(self):
        nw_interface = self.stack.network_interface_info(self._get_vm_id(), self._get_nw_interface_id())
        self.assertEqual(nw_interface['id'], self._get_nw_interface_id())

    def test_snapshot_list(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        snaps = self.stack.snapshot_list(self._get_vm_id())
        self.assertIn(snap, snaps)

    def test_snapshot_create(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.assertEqual(snap["name"], snap_name)

    def test_snapshot_info(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        snap = self.stack.snapshot_info(self._get_vm_id(), snap["id"])
        self.assertEqual(snap["name"], snap_name)

    def test_snapshot_revert(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.stack.snapshot_revert(self._get_vm_id(), snap["id"])

    def test_snapshot_delete(self):
        snap_name = "Snapshot:%f" % random.random()
        snap = self.stack.snapshot_create(self._get_vm_id(), snap_name)
        self.stack.snapshot_delete(self._get_vm_id(), snap["id"])
        snaps = self.stack.snapshot_list(self._get_vm_id())
        self.assertNotIn(snap, snaps)

    def test_tag_list(self):
        tag_name = "v0.0.1"
        guest_tags = self.stack.tag_create(self._get_vm_id(), tag_name)
        tags_list = self.stack.tag_list(self._get_vm_id())
        self.assertEqual(guest_tags, tags_list)

    def test_tag_create(self):
        # Waiting for vmware implementation
        return
        tag_name = "v0.0.1"
        guest_tags = self.stack.tag_create(self._get_vm_id(), tag_name)
        tags_list = self.stack.tag_list(self._get_vm_id())
        self.assertIn(tag_name, tags_list)

    def test_tag_delete(self):
        tag_name = "v0.0.1"
        self.stack.tag_create(self._get_vm_id(), tag_name)
        self.stack.tag_delete(self._get_vm_id(), tag_name)

        tags = self.stack.tag_list(self._get_vm_id())
        self.assertNotIn(tag_name, tags)
