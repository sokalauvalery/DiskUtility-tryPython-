"""Libraty for Non blocking reading from a subprocess output stream"""

from subprocess import *
import re

class InteractiveCommand:
    def __init__(self, process, prompt):
        """Class for Non blocking reading from a subprocess output stream

        Args:
            process (Popen): Object of class Popen.
            prompt (str): Console prompt
        """
        self.process = process
        self.prompt = prompt
        self.output = ""
        self.waitForPrompt()

    def waitForPrompt(self):
        """ Function waits while console prompt appears in output """
        while not self.prompt.search(self.output):
            c = self.process.stdout.read(1)
            if c == "":
                break
            self.output += c

        # Now we're at a prompt; clear the output buffer and return its contents
        tmp = self.output
        self.output = ""
        return re.sub(self.prompt, "", tmp).strip()

    def command(self, command):
        """ Write command in input stream
        :param command(str):
        :return: subprocess output
        """
        self.process.stdin.write(command + "\n")
        return self.waitForPrompt()