"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        # Instructions
        self.LDI_code = 0b10000010
        self.PRN_code = 0b01000111
        self.HLT_code = 0b00000001
        self.MUL_code = 0b10100010
        self.CALL_code = 0b01010000
        self.RET_code = 0b00010001

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if filename is not None:
            try:
                with open(filename) as file:
                    for line in file:
                        comment_split = line.split('#')
                        possible_instruction = comment_split[0]

                        if possible_instruction == '' or possible_instruction == '\n':
                            continue
                        instruction = int(possible_instruction, 2)

                        self.ram[address] = instruction
                        address += 1
                file.close()
                #print(self.ram)
            except IOError:
                print('There is no file at that location.')
                sys.exit(2)
        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8      ## Load immediate: Register 0 = 8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0        ## Print Register 0's value
                0b00000000,
                0b00000001, # HLT           ## Halt the program
            ]

            for instruction in program:
                self.ram[address] = instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        # Instruction register
        running = True
        while running:
            IR = self.ram[self.pc]
            if IR == self.LDI_code:
                print('LDI CODE')
                # Load immediate call. Set this data directly into a register for usage.
                register = self.ram[self.pc + 1]
                data = self.ram[self.pc + 2]
                self.reg[register] = data
                self.pc += 3

            elif IR == self.PRN_code:
                print('PRN CODE')
                # Print code, get the data out of the register given in the next instruction and print it.
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            
            elif IR == self.HLT_code:
                print('HLT CODE')
                running = False

            '''
            elif IR == self.MUL_code:
                

            elif IR = self.CALL_code:
                

            elif IR = self.RET_code:
            '''
            

