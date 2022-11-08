from Gui import Gui


class File:

    gui = None

    def start(self, gui):
        self.gui = gui

    def append(self, filename, contents):
        if self.gui.main_log_stuff:
            file = open(filename, "a")
            # Saving the array in a text file
            content = str(contents)
            file.write(content)
            file.close()