import sys
import io



class Tape :

    def __init__(self, start_values = [ "_" ], track = False):
        self._tape_head = 0
        self._tape_list = []
        self.track = track
        
        self._tape_length = len(start_values)

        for value in start_values :
            self._tape_list.append(str(value))

    def _extend_tape(self) :
        self._tape_list.append("_")
        self._tape_length += 1

    def move_right(self, multiple = 1, enroute = False) :
        
        for _ in range(multiple) :
            if self._tape_head >= self._tape_length - 1 :
                self._extend_tape()
            
            self._tape_head += 1

            if not enroute :
                self._track_me("move right")

    def move_left(self, multiple = 1, enroute = False) :
        for _ in range(multiple) :
            if self._tape_head > 0 :
                self._tape_head -= 1
            else : 
                self._tape_list = [" "] + self._tape_list
            
            if not enroute :
                self._track_me("move left")

    def get_value(self) :
        return self._tape_list[self._tape_head]
    
    def write_value(self, value) :
        self._tape_list[self._tape_head] = str(value)
        self._track_me(f"write {value}")
    
    def get_position (self) :
        return self._tape_head
    
    def moveto(self, line) :
        while line > self._tape_head :
            self.move_right(enroute = True)

        while line < self._tape_head :
            self.move_left(enroute = True)

        self._track_me(f"moveto {line}")

    def _track_me(self, message="") :
        if self.track :
            print(f"{message}")
            print(f"{self}\n")
            
            file = open(f"{sys.argv[1]}_output.txt", "a")
            file.write(f"{message}\n{self}\n")
            file.close()

    def __str__(self):
        str_rep = "end [ "
        str_hed = "      " 
        for line in range(self._tape_length) :
            value = self._tape_list[line]
            value_len = len(value)

            str_rep += f"{value} | "


            if self._tape_head == line :
                str_hed += f"V{" "*(value_len - 1)}"
            else :
                str_hed += f"{" "*(value_len + 3)}"
        
        return f"{str_hed}\n{str_rep} ..."


def read_code(filename) :
    code_lines = []
    with open(filename, "r") as file :
        file_lines = file.readlines()
        
        for line in file_lines :
            new_line = line.lower().strip()
            code_lines.append(new_line.split())

    return code_lines

def run_command(codeline, tape, line_number = 0) :
    code_tokens = codeline

    if len(code_tokens) > 0 and code_tokens[0] != "if" :

        # In this situation, the command comes with a conditional.
        condition = True
        command = code_tokens[0]

        # Some commands do not require arguments
        try :
            argument = code_tokens[1]
        except :
            argument = None


    elif len(code_tokens) > 0 : 
        # These commands are unconditional
        condition = (code_tokens[1] == tape.get_value())
        command = code[2]

        # Some commands do not require arguments
        try :
            argument = code_tokens[3]
        except :
            argument = None

    # In case the condition is met, continue. 
    # Note that here, if no conditional is provided, the default
    #  value of the conditional is True.
    if condition :

        if command == "moveto" :
            tape.moveto(int(argument))

        if command == "move" and argument[0] == "l" :
            tape.move_left()

        if command == "move" and argument[0] == "r" :
            tape.move_right()

        if command == "write" :
            tape.write_value(str(argument))
        

        # The next three dictate halt conditions, which can accept, reject, 
        #  or do neither
        if command == "halt" and argument == "accept":
            return True
        
        elif command == "halt" and argument == "reject" :
            return False
        
        elif command == "halt" :
            return -1

        if command == "goto" :
            return int(argument)
    
    return line_number + 1


def run_wb(codelines, tape=Tape(track=True)) :
    """
        This function receives a list of machine code isntructions,
            codelines
        and runs the commands one at a time on the provided tape.
            tape 
        If no tape is provided, it creates one for the commands to run on.
    """

    # The program is a sequence of commands, including comands that
    #  allow the user to jump between lines. This is why we keep track
    #  of line numbers.
    line_number = 0

    # While we are on a line that corresponds to a command
    while line_number >= 0 and line_number < len(codelines) :

        code = codelines[line_number]

        # The if/elif below checks if the code line is not blank,
        #  in which case we run the command on the code line.
        after_number = run_command(code, tape, line_number=line_number)

        if type(after_number) == bool :
            return after_number
        else : 
            line_number = after_number


if __name__ == "__main__" :
    print("\n"*20)

    try :
        inputfile = sys.argv[1]
        code = read_code(inputfile)
        with open(inputfile + "_output.txt", "w") as outputfile :
            print("Found", inputfile)
            outputfile.write("Running " + inputfile + "\n")

        try :
            start_tape = sys.argv[2]
            start_tape = list(start_tape)
            tape = Tape(start_tape, track=True)
        except :
            tape = Tape(track=True)

        print(f"Running code on\n{tape}\n\nStart:\n")
        run_wb(code, tape=tape)

    except :
        print("Entering interactive mode. After entering a starting string, run commands one at a time.")
        user_inp = input("Enter a starting string.\n")

        interact_tape = Tape(user_inp, track=False)
        command = ""

        while not ("quit" in user_inp or "quit" in command):
            print()
            print(interact_tape)
            command = input("> ")
            run_command(command, interact_tape)

        quit()