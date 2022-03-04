import pefile
from capstone import *
from capstone.x86 import *
import sys

class pe_anaylse:
    def __init__(self, path, function_offset, function_length):
        self.function_addr = 0
        self.section = 0
        self.path = path
        self.func_offset = function_offset
        self.cs = Cs(CS_ARCH_X86, CS_MODE_32)
        self.star_add = 0x0
        self.func_length = function_length
        self.code = "\x00"
        self.patch_byte = b"\xB8\x65\x00\x00\x00"

    def disass(self):
        for code in self.cs.disasm(self.code, self.function_addr, self.func_length):
            print("0x%x:\t%s\t%s" % (code.address, code.mnemonic, code.op_str))
        print("\npatch ->")
        for patch_code in self.cs.disasm(self.patch_byte, self.function_addr, len(self.patch_byte)):
            print("0x%x:\t%s\t%s" % (patch_code.address, patch_code.mnemonic, patch_code.op_str))

    def pe_find_text_section(self):
        pe = pefile.PE(self.path)
        for section in pe.sections:
            if ".text" in str(section.Name):
                self.section = section
                self.section_addr = section.VirtualAddress

    def pe_read(self):
        readfile = open(self.path, "rb+")
        code = readfile.seek(self.func_offset)
        self.code = readfile.read(self.func_length)
        readfile.close()

    def pe_patch(self):
        readfile = open(self.path, "rb+")
        code = readfile.seek(self.func_offset)
        self.code = readfile.write(self.patch_byte)
        readfile.close()


def patch_mana(file_path):
    patch_file = pe_anaylse(path=file_path, function_offset=0x4f370, function_length=0x6 + 1)
    patch_file.pe_read()
    patch_file.disass()
    patch_file.pe_patch()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("pls input the gamelogic.dll path")
        sys.exit(0)
    patch_mana(sys.argv[1])
