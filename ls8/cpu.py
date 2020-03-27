"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.SP = 7
        self.FL = 0b00000000

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        for line in (l.strip() for l in open(sys.argv[1]) if not l.startswith('#') and l.strip()):
            cmd = line[:8]
            self.ram[address] = int(cmd, 2)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.FL = 0b00000001
            if reg_a < reg_b:
                self.FL = 0b00000100
            if reg_a > reg_b:
                self.FL = 0b00000010
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
        MLT = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        JMP = 0b01010100
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110

        while 1 == 1:
            self.trace()
            command = self.ram[self.pc]
            if command == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PRN:
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])
                self.pc += 2
            elif command == MLT:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif command == PUSH:
                reg = self.ram[self.pc + 1]
                value = self.reg[reg]
                self.SP -= 1
                self.ram[self.SP] = value
                self.pc += 2
            elif command == POP:
                reg = self.ram[self.pc + 1]
                value = self.ram[self.SP]
                self.reg[reg] = value
                self.SP += 1
                self.pc += 2
            elif command == CALL:
                value = self.pc + 2
                reg = self.ram[self.pc + 1]
                subroutine = self.reg[reg]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = value
                self.pc = subroutine
            elif command == RET:
                pc = self.reg[self.SP]
                self.pc = self.ram[pc]
            elif command == ADD:
                self.alu('ADD', self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            elif command == JMP:
                self.pc = self.reg[self.ram_read(self.pc + 1)]
            elif command == CMP:
                self.alu('CMP', self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            elif command == JEQ:
                if self.E == 1:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2
            elif command == JNE:
                if self.E == 0:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2
            elif command == HLT:
                self.pc += 1
                break
            else:
                print(f'Unknown instruction: {command}')
                sys.exit(1)
