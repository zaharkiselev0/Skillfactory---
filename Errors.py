class QuitGameError(Exception):
    pass


class ShipCreateError(Exception):
    def __str__(self):
        return "Невозможно создать корабль. " + self.args[0]


class ShipAddError(Exception):
    def __str__(self):
        return "Невозможно разместить корабль. " + self.args[0]


class CommandError(Exception):
    pass


class HitError(CommandError):
    pass


class ScoutError(CommandError):
    pass


class UserInputError(Exception):
    pass
