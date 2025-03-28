from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from action.input_handlers import EventHandler
from entities.entity import Entity
from environment.game_map import GameMap


class Engine:

    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):
        
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov() # Update the FOV before the player's next action
    
    def update_fov(self) -> None:
        """
        Recompute the visible area based on the player's point of view
        """

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius = 8,
        )
        # If a tile is "visible" it should added to "explored"
        self.game_map.explored |= self.game_map.visible
    
    def render(self, console: Console, context: Context):

        self.game_map.render(console)

        context.present(console)

        console.clear()