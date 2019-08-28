"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        # Instructions
        self.LDI_code = 0b10000010
        self.PRN_code = 0b01000111
        self.HLT_code = 0b00000001

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

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
    
    def LDI(self, register, value):
        self.reg[register] = value

    def run(self):
        """Run the CPU."""
        instruction = self.ram[0] # Get the first instruction loaded in from the program.
        while instruction is not self.HLT_code: # While the instruction is not equal to HLT : 1
            if instruction == self.LDI_code:
                self.LDI()
            elif instruction == self.PRN_code:
                pass

