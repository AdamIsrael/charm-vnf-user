#!/usr/bin/env python3

import sys

sys.path.append("lib")

from charms.osm.ns import NetworkService

from ops.charm import CharmBase
from ops.main import main
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus,
    WaitingStatus,
    ModelError,
)

import random

class VnfUserCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        # Register all of the events we want to observe
        for event in (
            # Charm events
            self.on.install,
            self.on.upgrade_charm,
            # Charm actions (primitives)
            self.on.add_user_action,
        ):
            self.framework.observe(event, self)

    def on_install(self, event):
        """Called when the charm is being installed"""
        unit = self.model.unit

        unit.status = ActiveStatus()

    def on_upgrade_charm(self, event):
        """Upgrade the charm."""
        unit = self.model.unit

        # Mark the unit as under Maintenance.
        unit.status = MaintenanceStatus("Upgrading charm")

        self.on_install(event)

        # When maintenance is done, return to an Active state
        unit.status = ActiveStatus()

    ####################
    # NS Charm methods #
    ####################

    def on_add_user_action(self, event):
        username = event.params["username"]
        tariff = event.params["tariff"]

        # If this were a functional VNF, it would add the username to its
        # database. For demonstration purposes, this will return a random number
        user_id = random.randint(1, 100)

        event.set_results({"user-id": user_id})


if __name__ == "__main__":
    main(VnfUserCharm)

