class Console:
    __messages = []

    def add_message(self, message):
        self.__messages.append(message)

    def get_message(self, prompt):
        return input(prompt)

    def flush(self):
        for m in self.__messages:
            print(m)
        self.__messages = []
