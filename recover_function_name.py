import idaapi


def recover_function_name(handler_function_addr, function_offset):
    first_xref_addr = idaapi.get_first_fcref_to(handler_function_addr)
    next_xref_addr = first_xref_addr

    def get_string(addr):
        #print(addr)
        string = ""
        data_byte = idaapi.get_byte(addr)
        while data_byte:
            string = string + chr(data_byte)
            addr = addr + 1
            data_byte = idaapi.get_byte(addr)
        print(string)
        return string

    while next_xref_addr != 0xffffffff:
        print("a")
        #judge "push"
        if idaapi.get_byte(next_xref_addr - function_offset) != 0x68:
            next_xref_addr = idaapi.get_next_fcref_to(handler_function_addr, next_xref_addr)
            continue
        function_addr = idaapi.get_dword(next_xref_addr - function_offset + 1)
        function_name_offset = idaapi.get_dword(next_xref_addr - function_offset + 6)
        function_name = get_string(function_name_offset) + str(function_addr)
        
        # rename
        idaapi.set_name(function_addr, function_name)
        print(f"addr :{function_name_offset} {function_name} ")
        next_xref_addr = idaapi.get_next_fcref_to(handler_function_addr, next_xref_addr)

handler_function = {0xb5c130: 0xb, 0xA79610: 0xf}
for handler in handler_function.keys():
    recover_function_name(handler,handler_function[handler])
