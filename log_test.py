# Log chat

from __future__ import print_function
import frida
import sys

session = frida.attach("PwnAdventure3-Win32-Shipping.exe")
script = session.create_script("""
  //var chat = Module.findExportByName("PwnAdventure3-Win32-Shipping", "?Chat@Player@@UAEXPBD@Z");
  //var position_update_func_addr = ptr(Module.findBaseAddress('PwnAdventure3-Win32-Shipping.exe').add(0xe62bd0));
  //const position_update_func_addr = ptr(0x0E0E450);
  
  var exebaseAddr = Module.findBaseAddress('PwnAdventure3-Win32-Shipping.exe');
  var position_update_func_addr = resolveAddress("0x0E0E450");

  Interceptor.attach(position_update_func_addr,{
    onEnter: function(args){
        this.update_position_pointer = ptr(this.context.esp).add(0xc);
    },
    //asdasd
    onLeave: function (retval) {
      //console.log("esp",this.context.esp);
      //one esp value means one actor use esp to identify actors like rat.
      console.log("x"+Memory.readFloat(ptr(this.update_position_pointer)));
      console.log("y"+Memory.readFloat(ptr(this.update_position_pointer).add(4)));
      console.log("z"+Memory.readFloat(ptr(this.update_position_pointer).add(8)));
    }

  });


  var chat = DebugSymbol.load('GameLogic.dll')
  var chat = DebugSymbol.getFunctionByName('Player::Chat');
 
  Interceptor.attach(chat, {
      onEnter: function (args) { // 0 => this; 1 => cont char* (our text)
        var chatMsg = Memory.readCString(args[0]);
         //const myString = Memory.readUtf8String(args[1]);
         
         //console.log("[chat]:" + myString.toString());
         //console.log("[Chat]: " + chatMsg);
          //this.buf = args[1];
          //this.len = parseInt(args[2]);
          //log("ssl3_write(" + this.buf.toString() + ", " + this.len.toString() + ")");
          //var bbuf = Memory.readByteArray(this.buf, this.len);
          //console.log(chatMsg)
          //send(args[1].toString())
          readcommandLine(chatMsg+'')
         
      }
  });    
  
  var walkSpeed = DebugSymbol.getFunctionByName('Player::GetWalkingSpeed');
  var OnHealthUpdateEvent = DebugSymbol.getFunctionByName('GameServerConnection::OnHealthUpdateEvent');
  
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
              //this.Health = ptr(this.context.ecx).add(0xbc).sub(0xfc);
              //dumpAddr("health",this.Health,0x4);
              //Memory.writeInt(this.Health,102);
              //console.log("health"+Memory.readInt(this.Health));
              Memory.writeFloat(this.walkSpeedaddr,WalkSpeedHack);
              Memory.writeFloat(this.JumpSpeed,JumpSpeedHack);
              Memory.writeFloat(this.JumpHoldTime,JumpHoldTimeHack);
              //dumpAddr("player",ptr(this.Playeraddr).add(4).sub(0x48),0x148+0x20);

          },
          // Get the return value and write the new value
          onLeave: function (retval) {
              //console.log("speed: - "+Memory.readFloat(this.walkSpeedaddr));
              //Memory.writeFloat(this.walkSpeedaddr,99999);

          }
      });
  //cam't work
  Interceptor.attach(OnHealthUpdateEvent,
      {
          // Get Player * this location
          onEnter: function (args) {

            //console.log("health: "+Memory.readUInt(this.Healthaddr));
            //Memory.writeUInt(this.Healthaddr,0xfe);
            
          },
          // Get the return value and write the new value
          onLeave: function (retval) {
                //this.Healthaddr = ptr(this.context.ebp).sub(0xac);
                //dumpAddr("health",this.Healthaddr,64);
                //Memory.writeUInt(this.Healthaddr,101);
                //dumpAddr("health",this.Healthaddr,64);
              //console.log("speed: - "+Memory.readFloat(this.walkSpeedaddr));
              //Memory.writeFloat(this.walkSpeedaddr,99999);

          }
      });    
    //get local player object
    var  ClientWorld__AddLocalPlayer = DebugSymbol.getFunctionByName("ClientWorld::AddLocalPlayer");
    Interceptor.attach(ClientWorld__AddLocalPlayer,
        {
            onEnter: function(args){
                this.GameWorldaddr = this.context.ecx;
                
            },
            onLeave: function(retval){
              this.Playername = Memory.readCString(ptr(Memory.readUInt(ptr(this.GameWorldaddr).add(0x2c))).add(0x8));
                console.log("Player name :" + this.Playername);
                //console.log("Local Player's name :" + ptr(this.Playername).add(0x1e8));
            }
        });
    //
    var Actor__SetPosition = DebugSymbol.getFunctionByName("Actor::SetPosition");
    Interceptor.attach(Actor__SetPosition,
    {
        onEnter: function(args){
          console.log("set position");
        }
    });

    // Online players' objects create 
    var IPlayer__AddRef = DebugSymbol.getFunctionByName("IPlayer::AddRef");
    Interceptor.attach(IPlayer__AddRef,
        {
            onEnter: function(args){
                this.Playeraddr = this.context.ecx;
                this.Playername = Memory.readCString(ptr(this.Playeraddr).add(0x8));
                console.log("online Player's name :" + this.Playername);
                
                //console.log("POSITION:"+ Memory.readFloat(ptr(this.Playeraddr).add(0xd0)))
            }
        });

        var Player__UpdateState = DebugSymbol.getFunctionByName("Player::UpdateState");
        Interceptor.attach(Player__UpdateState,
        {
          onEnter: function(args){
              this.Player_ptr = this.context.ecx;
              //dumpAddr("player",ptr(this.Player_ptr).add(0x148),64);
              //console.log(this.Player_ptr);
              //console.log("POSITION:"+ Memory.readFloat(ptr(this.Player_ptr).add(0x148)) );
          }
        });
    var Enemy__Enemy = DebugSymbol.getFunctionByName("Enemy::Enemy");
    Interceptor.attach(Enemy__Enemy,
    {
            onEnter : function(args){
              console.log("create an enemy");
            }
    });

    // Online players' object destory
    var IPlayer__Release = DebugSymbol.getFunctionByName("IPlayer::Release");

    //tcp data
    var Socket_recv = Module.findExportByName('WS2_32.dll','recv');
    Interceptor.attach(Socket_recv,
        {
            onEnter: function(args){
                this.Socket_recv_buf = ptr(args[1]);
               
            },
            onLeave: function(retval){
               var data_len = retval.toInt32()-22;
               if(data_len>0)
               {
                 this.data_buf = this.Socket_recv_buf.add(22);
                 dumpAddr("data packages",this.data_buf,data_len);
               }
            }
        });

                    
    function dumpAddr(info, addr, size) {
        if (addr.isNull())
            return;

        console.log('Data dump ' + info + ' :');
        var buf = addr.readByteArray(size);

        // If you want color magic, set ansi to true
        console.log(hexdump(buf, { offset: 0, length: size, header: true, ansi: false }));
    };
    function resolveAddress(addr) {
        var idaBase = ptr('0x06B0000'); // Enter the base address of jvm.dll as seen in your favorite disassembler (here IDA)
        var offset = ptr(addr).sub(idaBase); // Calculate offset in memory from base address in IDA database
        var result = exebaseAddr.add(offset); // Add current memory base address to offset of function to monitor
        console.log('[+] New addr=' + result); // Write location of function in memory to console
        return result;
    }
  function readcommandLine(value) {
     console.log('[chat]:' + value);
     
     if( value.split(" ")[0] == "teleport") {
       console.log(value.split(" ")[1].split(','));
     } else {
     switch (value) {
     case "kill cows": 
           console.log("Killing all cows");
           break;
     case "teleport": 
           console.log("Killing all cows");
           break;   
     default:
     }
     }
  }     
 """)


def on_message(message, data):

  print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()


