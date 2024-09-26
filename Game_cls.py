from Player_cls import *
from CompStrategy_cls import *
from Gui_cls import *
import random
from itertools import *


class Game:
    def __init__(self, human: Player, comp: Player, comp_strategy: CompStrategy, gui: Gui,
                 ship_lenght: dict[int, int], player_commands):
        self.human = human
        self.comp = comp
        self.comp_strategy = comp_strategy
        self.gui = gui
        self.ship_lenght = ship_lenght
        self.player_commands = player_commands

    def params_from_str(self, params: list[str]):
        try:
            command = params[0]
            match command:
                case 'hit':
                    return [self.comp, Point(int(params[1]) - 1, int(params[2]) - 1)]
                case 'scout':
                    return [self.comp, int(params[1]), params[2] == '1']
        except Exception:
            raise UserInputError("Неверные параметры команды")
        raise UserInputError("Неизвестная команда")

    def run(self) -> None:
        self.gui.game_opening()
        while True:
            self.gui.draw()

            while True:
                try:
                    command_string = self.gui.command_request()
                    command = self.player_commands[command_string[0]]
                    params = self.params_from_str(command_string)
                    comm_response = command(self.human, *params)
                    break
                except (UserInputError, CommandError) as e:
                    self.gui.alertMessage(str(e))

            self.gui.command_response("human", comm_response)
            if not self.comp.grid.ships:
                self.gui.game_ending(win=True)
                break

            comm_response = self.comp_strategy.move(self.comp, self.human)
            self.gui.command_response("comp", comm_response)
            if not self.human.grid.ships:
                self.gui.game_ending(win=False)
                break
