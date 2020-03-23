"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        for line in (l.strip() for l in open(sys.argv[1]) if not l.startswith('#') and l.strip()):
            print(line[:8])
            cmd = f'0b{line[:8]}'
            self.ram[address] = cmd
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while 1 == 1:
            IR = self.reg[self.pc]
            command = self.ram[self.pc]
            if command == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] += operand_b
                self.pc += 3
            elif command == PRN:
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])
                self.pc += 2
            elif command == HLT:
                self.pc += 1
                break
            else:
                print(f'Unknown instruction: {command}')
                sys.exit(1)
