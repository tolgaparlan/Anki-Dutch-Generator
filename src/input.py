class InputReader:
    """Handles reading the input"""

    def __init__(self, mode, filename):
        self.filename = filename
        self.mode = mode

    def get_next_word(self) -> str:
        """
        Returns one word at a time from the input document
        :return: The next word
        """

        # The sub functions must be generators!!
        if self.mode == 'txt':
            return self.__get_txt_input()
        else:
            raise Exception("Unrecognized Mode")

    def __get_txt_input(self) -> str:
        """
        Reading a line each time from a txt file
        """
        with open(self.filename, 'r') as f:
            for line in f:
                yield line.strip()
