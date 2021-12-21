class Profile:
    def __init__(self, name: str, id_: int, raw_filename: str):
        # Input
        self.name = name
        self.id = id_
        self.raw_filename = raw_filename

        # Output
        self.id_filename = f"{self.id}.jpg" if self._is_valid() else None
        self.name_id_filename = f"{self.name}_{self.id}.jpg" if self._is_valid() else None

    def __repr__(self) -> str:
        return (
            f"{{raw_filename={self.raw_filename}, id_filename={self.id_filename}, "
            f"name_id_filename={self.name_id_filename}}}"
        )

    def _is_valid(self):
        if not self.raw_filename or type(self.raw_filename) != str:
            return False

        return True
