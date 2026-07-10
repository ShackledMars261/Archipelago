from test.bases import WorldTestBase

from .. import MIOWorld


class MIOTestBase(WorldTestBase):
    game = "Memories in Orbit"
    world: MIOWorld
