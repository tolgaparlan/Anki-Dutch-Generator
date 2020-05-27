class InputReader:
    """Handles reading the input"""

    def __init__(self, mode, filename):
        self.filename = filename
        self.mode = mode

    # Returns the input in a list, each element: {'Word':word}
    def getInput(self):
        if self.mode == 'txt':
            return self.__getTxtInput()
        else:
            raise Exception("Unrecognized Mode")

    def __getTxtInput(self):
        with open(self.filename, 'r') as f:
            return [{'Word': line.strip()} for line in f.readlines()]
