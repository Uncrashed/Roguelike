#!/usr/bin/env python3
import tcod

from engine import Engine
from action.input_handlers import EventHandler
from entities.entity import Entity
from environment.procgen import generate_dungeon

def main() -> None:

    screen_width = 80
    screen_heigth = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_room = 30


    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    player = Entity(int(screen_width/2), int(screen_heigth/2), "@", (255, 255, 255))
    npc = Entity(int(screen_width/2 - 5), int(screen_heigth/2),"@", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_heigth,
        tileset = tileset,
        title = "Yet Another Roguelike Tutorial",
        vsync = True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_width, order = "F")
        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)

if __name__ == "__main__":
    main()