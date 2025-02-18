class RISCAssembler:
    def __init__(self):
        self.opcodes = {
            'add': 0b0110011,
            'sub': 0b0110011,
            'or': 0b0110011,
            'and': 0b0110011,
            'srl': 0b0110011,
            'slt': 0b0110011,
            'addi': 0b0010011,
            'lw': 0b0000011,
            'jalr': 0b1100111,
            'sw': 0b0100011,
            'beq': 0b1100011,
            'bne': 0b1100011,
            'blt': 0b1100011,
            'jal': 0b1101111
        }
        
        self.funct3 = {
            'add': 0b000,
            'sub': 0b000,
            'and': 0b111,
            'or': 0b110,
            'slt': 0b010,
            'srl': 0b101,
            'addi': 0b000,
            'lw': 0b010,
            'jalr': 0b000,
            'sw': 0b010,
            'beq': 0b000,
            'bne': 0b001,
            'blt': 0b100
        }
        
        self.funct7 = {
            'add': 0b0000000,
            'sub': 0b0100000,
            'or': 0b0000000,
            'and': 0b0000000,
            'srl': 0b0000000,
            'slt': 0b0000000,
            'addi': 0b0000000,
            'lw': 0b0000000,
            'jalr': 0b0000000,
            'sw': 0b0000000,
            'beq': 0b0000000,
            'bne': 0b0000000,
            'blt': 0b0000000,
            'jal': 0b0000000
        }
        
        self.registers = {
            'zero': 0,
            'ra': 1,
            'sp': 2,
            'gp': 3,
            'tp': 4,
            't0': 5,
            't1': 6,
            't2': 7,
            's0': 8,
            's1': 9,
            'a0': 10,
            'a1': 11,
            'a2': 12,
            'a3': 13,
            'a4': 14,
            'a5': 15,
            'a6': 16,
            'a7': 17,
            's2': 18,
            's3': 19,
            's4': 20,
            's5': 21,
            's6': 22,
            's7': 23,
            's8': 24,
            's9': 25,
            's10': 26,
            's11': 27,
            't3': 28,
            't4': 29,
            't5': 30,
            't6': 31,
        }

        self.labels = {
        }

    def assemble(self, address, instruction):
        instruction = instruction.replace(',', ' ').replace(':', ' ').replace("(", " ").replace(")", " ")
        parts = instruction.split()
        if len(parts) == 5:
            self.labels[parts[0]] = address
            parts.pop(0)
        if len(parts) < 4 or parts[0] not in self.opcodes:
            raise ValueError("Invalid instruction format")
        

        opcode = self.opcodes[parts[0]]
        if parts[0] in ['beq', 'blt', 'bne']:
            # B-Type instruction
            opcode = self.opcodes[parts[0]]
            funct3 = self.funct3[parts[0]]
            rs1 = self.registers[parts[1]]
            rs2 = self.registers[parts[2]]
            if (parts[3] == '0'):
                offset = 0
            else:
                offset = (self.labels[parts[3]] - address) >> 1
            imm = format(offset & 0xFFF, '012b')
            imm1 = int(imm[0], 2)
            imm2 = int(imm[2:8], 2)
            imm3 = int(imm[8:12], 2)
            imm4 = int(imm[1], 2)
            return '{:032b}'.format(imm4 << 31|imm2 << 25|rs2 << 20|rs1 << 15|funct3 << 12|imm3 << 8|imm4 << 7|opcode)

        raise ValueError("Unsupported instruction")

# Example usage
assembler = RISCAssembler()

file = r"test0.txt"
with open(file, 'r') as f:
    address = 0x1000
    for line in f:
        print(assembler.assemble(address, line))
        address+=4
