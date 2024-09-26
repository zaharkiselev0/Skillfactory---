from abc import ABCMeta, abstractmethod
from CommandResponse_cls import *
from Errors import *


class Gui:
    def __init__(self, commands: frozenset[str]):
        self.commands = commands

    @abstractmethod
    def game_opening(self) -> None:
        pass

    @abstractmethod
    def game_ending(self, win: bool) -> None:
        pass

    @abstractmethod
    def help(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def set_opening() -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_ship(length: int) -> str:
        pass

    @abstractmethod
    def ship_set(self, points: list[list[int]], print_message: bool) -> None:
        pass

    @staticmethod
    @abstractmethod
    def set_ending() -> None:
        pass

    @abstractmethod
    def command_request(self) -> list[str]:
        pass

    @abstractmethod
    def command_response(self, player_type: str, resp: CommandResponse) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_bool(message: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def alertMessage(message: str) -> None:
        pass

class ConsoleGui(Gui):
    def __init__(self, commands, row_num, col_num):
        super().__init__(commands)
        self.gui_commands = {'help': self.help, 'quit': self.quit}
        self.ship_matrix = [['0'] * col_num for _ in range(row_num)]
        self.hit_matrix = [['0'] * col_num for _ in range(row_num)]
        self.row_num = row_num
        self.col_num = col_num
        self.ship_char = '■'
        self.hit_char = 'X'
        self.miss_char = 'T'
        self.scout_success = 'S'
        self.scout_fail = 'F'

    def game_opening(self) -> None:
        print("Игра началась")

    def help(self, command: str = '') -> None:
        if not command:
            return print("После размещения кораблей игрок каждый ход вводит команды."
                         "Некоторые команды могут иметь параметры."
                         "Параметры вводятся в строке с командой через пробел."
                         "Пример: hit 1 3 - выстрелить в точку с координатами (1, 3)\n"
                         "Координаты точек игрового поля индексируются с 1.\n"
                         f"Список доступных команд: {' '.join(self.commands)} {' '.join(self.gui_commands.keys())}\n"
                         "Для вывода этой справки введите: help\n"
                         "Для вывода продробной информации о команде и ее параметрах введите:help [имя команды]\n")

        match command:
            case 'hit':
                return print("Команда hit:\n"
                             "Сделать выстрел в точку с заданными координатами."
                             "Синтаксис:hit [номер строки] [номер столбца]\n"
                             "Пример:hit 1 3 - выстрелить в точку с координатами (1, 3)\n")
            case 'quit':
                return print("Команда quit: Закончить игру и начать новую\n")

            case 'scout':
                return print("Команда scout:\n"
                             "Узнать состояние вражеских клеток заданной строки(заняты кораблем или пусты)."
                             "Пустые клетки будут отображаться на карте символом F, занятые - S."
                             "При этом уничтожается случайный собственный корабль.\n"
                             "Синтаксис:scout [номер строки] [1 или 0]\n"
                             "Если второй параметр равен 1 будет разведана строка, если 0 - столбец\n"
                             "Пример:scout 4 0 - узнать состояние вражеских клеток 4-ой строки\n")
            case _:
                print("Неизвестная команда")

    def game_ending(self, win: bool) -> None:
        if win:
            print("Конец игры. Вы победили")
        else:
            print("Конец игры. Вы проиграли")

    def draw(self) -> None:
        player_ship = ['  | ' + ' | '.join(map(str, range(1, self.col_num + 1)))]
        for i in range(1, self.row_num + 1):
            player_ship.append(str(i) + ' | ' + ' | '.join(self.ship_matrix[i - 1]))

        comp_ships = ['  | ' + ' | '.join(map(str, range(1, self.col_num + 1)))]
        for i in range(1, self.row_num + 1):
            comp_ships.append(str(i) + ' | ' + ' | '.join(self.hit_matrix[i - 1]))

        print((self.col_num * 2 - 6) * ' ' + "Ваши корабли:" + (self.col_num * 4 - 3) * ' ' + "Корабли соперника: ")
        for player_string, comp_string in zip(player_ship, comp_ships):
            print(player_string, comp_string, sep='           ')

    @staticmethod
    def set_opening() -> None:
        print("Вам нужно разместить корабли")

    @staticmethod
    def get_ship(length: int) -> list[str]:
        print(f"Размещение корабля длины {length}")
        start = input("Введите через пробел координаты начала корабля: ")
        end = input("Введите через пробел координаты конца корабля: ")
        return [start, end]

    def ship_set(self, points: list[list[int]], print_message: bool) -> None:
        for x, y in points:
            self.ship_matrix[x][y] = self.ship_char
        if print_message:
            print("Корабль успешно размещен")

    def set_ending(self) -> None:
        print("Все корабли успешно размещены")

    @staticmethod
    def get_bool(message: str) -> bool:
        ans = input(message + '[д/н]:')
        while ans not in ['д', 'н', 'l', 'y']:
            print('Неверный символ, введите д(да) или н(нет)')
            ans = input(message + '[д/н]:')
        return ans == 'д' or ans == 'l'

    def command_request(self) -> list[str]:
        try:
            command_string, *params = input("Введите команду:").split()
        except ValueError:
            raise UserInputError(f"Вы ничего не ввели. Доступные команды: {' '.join(self.commands)}")

        while command_string in self.gui_commands:
            command = self.gui_commands[command_string]
            command(*params)
            command_string, *params = input("Введите команду:").split()

        if command_string not in self.commands:
            raise UserInputError(f"Неверная команда. Доступные команды: {' '.join(self.commands)} {' '.join(self.gui_commands)}")

        return [command_string, *params]

    def command_response(self, player_type: str, resp: CommandResponse) -> None:
        is_human = player_type == "human"
        match resp.response_type:

            case ResponseType.HIT_MISS:
                if is_human:
                    print("Вы промахнулись")
                    self.hit_matrix[resp.x][resp.y] = self.miss_char
                else:
                    print(f"Копьтер выстрелил в клетку {resp.x + 1, resp.y + 1} и промахнулся")
                    self.ship_matrix[resp.x][resp.y] = self.miss_char

            case ResponseType.HIT_GOT:
                if is_human:
                    print("Вы попали")
                    self.hit_matrix[resp.x][resp.y] = self.hit_char
                else:
                    print(f"Копьтер выстрелил в клетку {resp.x + 1, resp.y + 1} и попал")
                    self.ship_matrix[resp.x][resp.y] = self.hit_char

            case ResponseType.HIT_KILL:
                if is_human:
                    print("Вы попали и уничтожили корабль")
                    self.hit_matrix[resp.x][resp.y] = self.hit_char
                else:
                    print(f"Копьтер выстрелил в клетку {resp.x + 1, resp.y + 1} и уничтожил ваш корабль")
                    self.ship_matrix[resp.x][resp.y] = self.hit_char

            case ResponseType.SCOUT:
                if is_human:
                    for x, y in resp.ship_points:
                        self.ship_matrix[x][y] = self.hit_char
                    for (x, y), success in zip(resp.cords_to_scout, resp.scout_points):
                        if self.hit_matrix[x][y] == '0':
                            self.hit_matrix[x][y] = self.scout_success if success else self.scout_fail
                    print("Вы разведали территорию")
                else:
                    raise NotImplementedError("команда scout не реализована для компьютера")

    def quit(self):
        raise QuitGameError()

    @staticmethod
    def alertMessage(message: str) -> None:
        print(message)
