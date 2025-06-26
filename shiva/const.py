# Copyright (c) 2024 Boris Soldatov
# SPDX-License-Identifier: MIT
#
# This file is part of an open source project licensed under the MIT License.
# See the LICENSE file in the project root for more information.

SHIVA_ROOT = 'shiva'

MODULES_COMMANDS = 'commands'
MODULES_DRIVERS = 'drivers'
MODULES_WORKERS = 'workers'
MODULES_DISPATCHERS = 'dispatchers'
MODULES_TYPES = 'data_types'
MODULES_PROTO = 'proto'


SCOPES = [
    # MODULES_COMMANDS, Typer handling commands
    MODULES_DRIVERS,
    MODULES_WORKERS,
    MODULES_DISPATCHERS,
    MODULES_TYPES,
    MODULES_PROTO,
]

CLI_SCOPES = [
    MODULES_DRIVERS,
]

MSG_ACK = 0
MSG_NACK = 1
MSG_REJECT = 2
