class InputReader:
    """Handles reading the input"""

    def __init__(self, mode, filename):
        self.filename = filename
        self.mode = mode

    # Returns one word as {'Word':word}
    # The sub functions must be generators!!
    def getLine(self):
        if self.mode == 'txt':
            return self.__getTxtInput()
        else:
            raise Exception("Unrecognized Mode")

    # Reading a line each time from a txt file
    def __getTxtInput(self):
        with open(self.filename, 'r') as f:
            for line in f:
                yield line.split()
