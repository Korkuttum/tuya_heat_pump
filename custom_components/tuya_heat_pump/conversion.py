class Conversion:
    def __init__(self, conversion: str) -> None:
        self.conversion = conversion

    def convert(self, value):
        return eval(
            self.conversion,
            {
                "value": value,
                "__builtins__": {
                    "bool": bool,
                    "float": float,
                    "int": int,
                },
            },
        )
