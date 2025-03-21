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
        
    def int_to_5bit_binary(self, n):
        if n < 0 or n > 31:
            raise ValueError("Input must be between 0 and 31 (inclusive) for 5-bit representation.")
        binary = ''
        for i in range(5):
            binary = str(n % 2) + binary  
            n //= 2  
        return binary
    
    def to_12bit_binary(self, offset):
        if not (-2048 <= offset <= 2047):
            raise ValueError("Offset out of 12-bit range (-2048 to 2047)")
        
        if offset < 0:
            offset = (2 ** 12) + offset
        
        binary = ""
        for _ in range(12):
            binary = str(offset % 2) + binary
            offset = offset // 2 
    
        return binary

    def assemble(self, labels, address, instruction):
        instruction = instruction.replace(',', ' ').replace(':', ' ').replace("(", " ").replace(")", " ")
        parts = instruction.split()
        
        if len(parts) == 5:  
            parts.pop(0)
        if len(parts) == 4 and "jal" in parts:
            parts.pop(0)
        if parts[0] not in self.opcodes:
            raise ValueError("Invalid instruction format")
        
        opcode = self.opcodes[parts[0]]
        
        # B-Type instructions
        if parts[0] in ['beq', 'blt', 'bne']:
            funct3 = self.funct3[parts[0]]
            rs1 = self.registers[parts[1]]
            rs2 = self.registers[parts[2]]
            offset_str = parts[3]
            if offset_str in labels:
                label_address = labels[offset_str]
                offset = (label_address - address) >> 1
            else:
                offset = int(offset_str) >> 1

            imm = format(offset & 0xFFF, '012b')           
            imm1 = int(imm[0], 2)
            imm2 = int(imm[2:8], 2)
            imm3 = int(imm[8:12], 2)
            imm4 = int(imm[1], 2)
            return '{:032b}'.format(imm1 << 31 | imm2 << 25 | rs2 << 20 | rs1 << 15 | funct3 << 12 | imm3 << 8 | imm4 << 7 | opcode)
            
        # R-Type instructions
        elif parts[0] in ['add', 'sub', 'and', 'or', 'srl', 'slt']:
            opcode = '0110011'
            mnemonic = parts[0]
            if mnemonic not in self.opcodes:
                raise ValueError("Unsupported R-type Instructions: ", mnemonic)
            rd_bin = self.registers[parts[1]]
            rs1_bin = self.registers[parts[2]]
            rs2_bin = self.registers[parts[3]]
    
            funct7 = self.funct7[mnemonic]
            funct7 = '{:07b}'.format(int(funct7))
            funct3 = self.funct3[mnemonic]
            funct3 = '{:03b}'.format(int(funct3))
    
            binary = f"{funct7}{self.int_to_5bit_binary(rs2_bin)}{self.int_to_5bit_binary(rs1_bin)}{funct3}{self.int_to_5bit_binary(rd_bin)}{opcode}"
            
            if len(binary) != 32:
                raise ValueError(f"Generated binary has invalid length: {len(binary)} bits")
            
            return binary
        
        # S-Type instructions
        elif parts[0] in ['sw']:
            opcode = '0100011'
            mnemonic = parts[0]
            if mnemonic not in self.opcodes:
                raise ValueError("Unsupported S-type Instructions: ", mnemonic)
            rs2 = parts[1]
            offset = parts[2]
            rs1 = parts[3]

            rs1_bin = self.int_to_5bit_binary(self.registers[rs1])
            rs2_bin = self.int_to_5bit_binary(self.registers[rs2])

            funct3 = self.funct3[mnemonic]
            funct3 = '{:03b}'.format(int(funct3))

            imm = self.to_12bit_binary(int(offset))
            imm_11_5 = imm[:7]
            imm_4_0 = imm[7:]
            binary = f"{imm_11_5}{rs2_bin}{rs1_bin}{funct3}{imm_4_0}{opcode}"
            
            if len(binary) != 32:
                raise ValueError(f"Generated binary has invalid length: {len(binary)} bits")
    
            return binary
        
        # J-Type instructions (jal)
        elif parts[0] in ['jal']:
            rd = self.registers[parts[1]]
            target = parts[2]

            if target in labels:
                label_address = labels[target]
                offset = label_address - address
            else: 
                offset = int(target)

            imm_20 = (offset >> 20) & 0x1       
            imm_10_1 = (offset >> 1) & 0x3FF    
            imm_11 = (offset >> 11) & 0x1       
            imm_19_12 = (offset >> 12) & 0xFF  

            binary_instruction = (imm_20 << 31) | (imm_19_12 << 12) | (imm_11 << 20) | (imm_10_1 << 21) | (rd << 7) | opcode
            
            return '{:032b}'.format(binary_instruction)
        
        # I-Type instructions
        elif parts[0] in ['addi', 'lw', 'jalr']:
            if parts[0] == 'lw':
                funct3 = self.funct3[parts[0]]
                rd = self.registers[parts[1]]
                rs1 = self.registers[parts[3]]
                imm = int(parts[2]) & 0xFFF
            else:
                funct3 = self.funct3[parts[0]]
                rd = self.registers[parts[1]]
                rs1 = self.registers[parts[2]]
                imm = int(parts[3]) & 0xFFF  
            
            binary_instruction = (imm << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | opcode
            
            return '{:032b}'.format(binary_instruction)

        raise ValueError("Unsupported instruction")
        
# Example usage
assembler = RISCAssembler()

input_file = r"C:\Users\Mritunjay\OneDrive\Desktop\test0.txt"
output_file = r"C:\Users\Mritunjay\OneDrive\Desktop\output.txt"
labels = {}

with open(input_file, 'r') as f:
    address = 0x1000
    for line in f:
        line = line.replace(',', ' ').replace(':', ' ').replace("(", " ").replace(")", " ")
        parts = line.split()
        labels[parts[0]] = address
        address += 4

with open(output_file, 'w') as out_f:
    address = 0x1000
    with open(input_file, 'r') as f:
        for line in f:
            binary_instruction = assembler.assemble(labels, address, line)
            out_f.write(binary_instruction + '\n')
            address += 4
