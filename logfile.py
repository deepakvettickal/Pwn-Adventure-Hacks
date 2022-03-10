# Log chat

from __future__ import print_function
import frida
import sys

session = frida.attach("PwnAdventure3-Win32-Shipping.exe")
script = session.create_script("""
        var exebaseAddr = Module.findBaseAddress('PwnAdventure3-Win32-Shipping.exe');
        var position_update_func_addr = resolveAddress("0x0E0E450");

        Interceptor.attach(position_update_func_addr, {
            onEnter: function (args) {
                this.update_position_pointer = ptr(this.context.esp).add(0xc);
            },
            //asdasd
            onLeave: function (retval) {
                //console.log("esp",this.context.esp);
                //one esp value means one actor use esp to identify actors like rat.
                console.log("x" + Memory.readFloat(ptr(this.update_position_pointer)));
                console.log("y" + Memory.readFloat(ptr(this.update_position_pointer).add(4)));
                console.log("z" + Memory.readFloat(ptr(this.update_position_pointer).add(8)));
            }

        });




        var chat = DebugSymbol.load('GameLogic.dll')
        var walkSpeed = DebugSymbol.getFunctionByName('Player::GetWalkingSpeed');
        //console.log("Player::GetWalkingSpeed() at address: " + walkSpeed);
        var walkSpeedOffset = 0x120;
        var JumpHoldTimeOffset = 0x128;
        var JumpSpeedHoldTimeOffset = 0x124;

        var WalkSpeedHack = 9999;
        var JumpSpeedHack = 9999;
        var JumpHoldTimeHack = 60;
        // Check Speed
        Interceptor.attach(walkSpeed,
            {
                // Get Player * this location
                onEnter: function (args) {
                    //use the Player pointer this = $ecx, therefore only need hook one funciton and modify all valure by using this pointer

                    this.walkSpeedaddr = ptr(this.context.ecx).add(walkSpeedOffset);
                    this.JumpHoldTime = ptr(this.context.ecx).add(JumpHoldTimeOffset);
                    this.JumpSpeed = ptr(this.context.ecx).add(JumpSpeedHoldTimeOffset);
                    this.Health = ptr(this.context.ecx).add(0xbc).sub(0xfc);
                    //dumpAddr("health",this.Health,0x4);
                    Memory.writeInt(this.Health, 102);
                    //console.log("health"+Memory.readInt(this.Health));
                    Memory.writeFloat(this.walkSpeedaddr, WalkSpeedHack);
                    Memory.writeFloat(this.JumpSpeed, JumpSpeedHack);
                    Memory.writeFloat(this.JumpHoldTime, JumpHoldTimeHack);

                },
                // Get the return value and write the new value
                onLeave: function (retval) {
                    //console.log("speed: - "+Memory.readFloat(this.walkSpeedaddr));
                    //Memory.writeFloat(this.walkSpeedaddr,99999);

                }
            });

        var IPlayer__AddRef = DebugSymbol.getFunctionByName("IPlayer::AddRef");
        Interceptor.attach(IPlayer__AddRef,
            {
                onEnter: function(args){
                    this.Playeraddr = this.context.ecx;
                    this.Playername = Memory.readCString(ptr(this.Playeraddr).add(0x8));
                    console.log("online Player's name :" + this.Playername);
                    
                }
            });

        var chat = DebugSymbol.getFunctionByName('Player::Chat');
        //var location = DebugSymbol.getFunctionByName('Player::GetLookPosition');
        let that = this;
        var playerPosMemObj = { x: 0, y: 0, z: 0 };
        CalculatePositionPointers();

        // Chat function implementation
        Interceptor.attach(chat, {
            onEnter: function (args) { // 0 => this; 1 => cont char* (our text)
                var chatMsg = Memory.readCString(args[0]);
                readcommandLine(chatMsg + '')

            }
        });




        // pasing the data in chat command line 
        function readcommandLine(value) {
            console.log('[chat]:' + value);

            if (value.split(" ")[0] == "teleport") {
                var coord = value.split(" ")[1].split(',');
                console.log(coord)
                Memory.writeFloat(playerPosMemObj['x'], parseFloat(coord[0]));
                Memory.writeFloat(playerPosMemObj['y'], parseFloat(coord[1]));
                Memory.writeFloat(playerPosMemObj['z'], parseFloat(coord[2]));
                console.log('Teleporting to location: ' + coord);
                console.log(Memory.readFloat(playerPosMemObj['x']))
                console.log(Memory.readFloat(playerPosMemObj['y']))
                console.log(Memory.readFloat(playerPosMemObj['z']))
            }
        }

        function CalculatePositionPointers() {
            var baseptr = Module.findBaseAddress("GameLogic.dll")
            var step1 = Memory.readPointer(ptr(baseptr).add('0x0097D7C'))
            var step2 = Memory.readPointer(ptr(step1).add('0x1C'))
            var step3 = Memory.readPointer(ptr(step2).add('0x64'))
            var step4 = Memory.readPointer(ptr(step3).add('0x48'))
            var step5 = Memory.readPointer(ptr(step4).add('0x4'))
            var step6 = Memory.readPointer(ptr(step5).add('0x288'))
            var step7 = Memory.readPointer(ptr(step6).add('0xB4'))
            var finalStep = ptr(step7).add('0x98')
            playerPosMemObj['x'] = ptr(ptr(finalStep).sub(8))
            playerPosMemObj['y'] = ptr(ptr(finalStep).sub(4))
            playerPosMemObj['z'] = ptr(finalStep);
            console.log(Memory.readFloat(playerPosMemObj['x']))
            console.log(Memory.readFloat(playerPosMemObj['y']))
            console.log(Memory.readFloat(playerPosMemObj['z']))
        }


        function getValueAtMemWithOffset(baseMemory, offset) {
            return Memory.readUInt(ptr((baseMemory) + offset));
        }
        function resolveAddress(addr) {
            var idaBase = ptr('0x06B0000'); // Enter the base address of jvm.dll as seen in your favorite disassembler (here IDA)
            var offset = ptr(addr).sub(idaBase); // Calculate offset in memory from base address in IDA database
            var result = exebaseAddr.add(offset); // Add current memory base address to offset of function to monitor
            console.log('[+] New addr=' + result); // Write location of function in memory to console
            return result;
        }       
 """)


def on_message(message, data):

  print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()
