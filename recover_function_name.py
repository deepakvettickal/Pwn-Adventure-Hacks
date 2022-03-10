import idaapi


def recover_function_name(handler_function_addr, function_offset):
    first_xref_addr = idaapi.get_first_fcref_to(handler_function_addr)
    next_xref_addr = first_xref_addr

    def get_string(addr):
        string = ""
        data_byte = idaapi.get_byte(addr)
        while data_byte:
            string = string + chr(data_byte)
            addr = addr + 1
            data_byte = idaapi.get_byte(addr)
        print(string)
        return string

    while next_xref_addr != 0xffffffff:
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
"""
first function addr :
.text:004CBF5F                               loc_4CBF5F:                             ; CODE XREF: sub_4CB7F0+74C↑j
.text:004CBF5F 68 D0 EF 4E 00                push    offset sub_4EEFD0
.text:004CBF64 68 10 F6 5D 01                push    offset aGetmana_0               ; "GetMana"
.text:004CBF69 50                            push    eax
.text:004CBF6A E8 C1 01 0E 00                call    sub_5AC130

=> 0x5ac130:0xb

second fucntion addr :
.text:004CB7F0
.text:004CB7F0 83 EC 08                      sub     esp, 8
.text:004CB7F3 68 50 C6 4E 00                push    offset sub_4EC650
.text:004CB7F8 68 D8 47 5E 01                push    offset aActivateitemfr_0        ; "ActivateItemFromInventory"
.text:004CB7FD 68 48 A3 5D 01                push    offset aScriptPwnadven          ; "/Script/PwnAdventure3"
.text:004CB802 E8 09 DE FF FF                call    sub_4C9610
.text:004CB802

=>0x4c9610:0xf

address may change due to debugging
"""
handler_function = {0xb5c130: 0xb, 0xA79610: 0xf}
for handler in handler_function.keys():
    recover_function_name(handler,handler_function[handler])
