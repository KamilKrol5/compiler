class LabelProvider:
    def __init__(self, initial_label: str):
        self.counter = 0
        self.initial_label = initial_label

    def get_label(self) -> str:
        self.counter = self.counter + 1
        return self.initial_label + str(self.counter)
