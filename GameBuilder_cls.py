from Game_cls import *
from typing import Optional


class GameBuilder:
    ship_lenght_base = {3: 1, 2: 2, 1: 4}
    width_base = 6
    height_base = 6

    ship_lenght_extended = {3: 2, 2: 2, 1: 5}
    width_extended = 9
    height_extended = 9

    randomStrategy = RandomHitStrategy()
    randomStrategyImproved = RandomHitImproved()

    def __init__(self, gui_cls):
        self.gui_cls = gui_cls

    def setup(self):
        self.width = GameBuilder.width_base
        self.height = GameBuilder.height_base
        self.ship_length = GameBuilder.ship_lenght_base
        self.comp_strategy = GameBuilder.randomStrategy
        self.commands = {'hit': Player.hit}
        if not self.gui_cls.get_bool("Играть со стандартными настройками?"):
            if self.gui_cls.get_bool("Играть на большом поле?"):
                self.width = GameBuilder.width_extended
                self.height = GameBuilder.height_extended
                self.ship_length = GameBuilder.ship_lenght_extended
            if self.gui_cls.get_bool("Играть с продвинутым ии?"):
                self.comp_strategy = GameBuilder.randomStrategyImproved
            if self.gui_cls.get_bool("Добавить дополнительные действия для игрока?"):
                self.commands['scout'] = Player.scout
                self.gui_cls.help(None, 'scout')

    def getGame(self):
        game = Game(Player(self.height, self.width), Player(self.height, self.width),
                    self.comp_strategy, self.gui_cls(self.commands.keys(), self.height, self.width),
                    self.ship_length, self.commands)
        self.randomSetShips(game.comp, self.ship_length, )
        if game.gui.get_bool("Разместить корабли случайно?"):
            self.randomSetShips(game.human, self.ship_length, game.gui)
        else:
            self.guiSetShips(game.human, self.ship_length, game.gui)
        return game

    def run(self):
        self.setup()
        game = self.getGame()
        game.gui.help()
        while True:
            try:
                game.run()
            except QuitGameError:
                pass
            if not self.gui_cls.get_bool("Начать новую игру с текущими настройками?"):
                self.setup()
            game = self.getGame()

    @staticmethod
    def guiSetShips(player: Player, ship_lenght: dict[int, int], gui: Gui):
        gui.set_opening()
        for length, num in ship_lenght.items():
            for _ in range(num):
                while True:
                    try:
                        start, end = gui.get_ship(length)
                        start_point = Point(*map(int, start.split())) - Point(1, 1)
                        end_point = Point(*map(int, end.split())) - Point(1, 1)
                        ship = Ship(start_point, end_point)
                        if ship.health != length:
                            raise ShipAddError(f"Неверная длина корабля - {ship.health}")
                        ship_points = [[p.x, p.y] for p in ship.points()]
                        player.add(ship)
                        gui.ship_set(ship_points, True)
                        break
                    except (ValueError, TypeError):
                        gui.alertMessage("Невверные данные. Введите 2 числа через пробел")
                    except (ShipAddError, ShipCreateError) as e:
                        gui.alertMessage(str(e))

        gui.set_ending()

    @staticmethod
    def randomSetShips(player: Player, ship_lenght: dict[int, int], gui: Optional[Gui] = None):
        points = cycle(player.hits.keys())
        for length, num in sorted(ship_lenght.items(), reverse=True):
            for _ in range(num):
                while True:
                    try:
                        start_point = next(points)
                        shift = Point(0, length - 1) if random.choice([True, False]) else Point(length - 1, 0)
                        end_points = start_point + shift
                        ship = Ship(start_point, end_points)
                        if ship.health != length:
                            raise ShipAddError(f"Неверная длина корабля - {ship.health}")
                        player.add(ship)
                        if gui:
                            ship_points = [[p.x, p.y] for p in ship.points()]
                            gui.ship_set(ship_points, False)
                        break
                    except ShipAddError:
                        pass
        if gui:
            gui.set_ending()
