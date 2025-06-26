import random

logo_0_120= """
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                                           .+.                                                          
                                                  `.      /oos/`      .`                                                
                                         `.      ./++-`  `+ssso`   `:+o/.                                               
                                        `-+:/.  `//oo+    :ooo/    -oo++-   `.-:/                                       
                                 .      `/++/:   .oys+:://+yss/::---sso/`   -+oo+.                                      
                                `///:.  `-+yso+oossyyyssssssooss++++/+o+/:-.+o++/`  `.:-:                               
                                `/+o+/`.:+syhyyyyyyyyhyhhhdhhhhhhhyyssoo+++/++o/.`  :oo++`                              
                         .`.``   -/ssysyyyyyyhhhyyyyyyssyoyyyysos+ssshyyyyyso++/+/:-so+/:    `                          
                         -+:/-. `:oyyyyyyhhyysoo/:-.....yhhhyhyys-....-:/+osyyyyso+++o+-   -/+:+`                       
                         ./+o+++syyyhhhyyso/-..`````    /yyhyyyys`    .::::++oooyyhyo++++--ooo/+`                       
                   ` ```  .-oyyyyhhyyso/-``..-.``.``   ``+ys+osss`    ````.-:-/oo+oyyhysoosss+/-                        
                   -+//:. .+ysyhhyso/.` ..-`  `````.` :++osyhyyyo/.` ```````  `:.+//+syhhsoos/`  .-:..`                 
                   `/+oo++ssyyhys+-`  `-. ````...`.`..:oyooso+osso/` ````````     ::`-+syhhysso--+oo/+                  
                    `-:sysyhhys+.     :-`````.`````..-///+oso/:oso/.`````  `````````. `-/syhhhsysyo++.                  
              ``.``  `/ssyhhs+-      --`````-`..```..:/o+syssooshso..``````.```     .`  `-+soo+syy+.`                   
              .://+/.ossyhhs:`       :/o-.`.-``.`.```.+hyoosoysyysy-````````  .```````    `/oooshyy/ .://`.             
              `:/+oyssshhyo-        .ooos+` .``.`.``.--/hossosyoso:````````.```  ````   .:++ooyhdhyy+o/o+o.             
               `..:ysyhhyo.        `+oo+/.``.:..` ``.`.-sddhysyhhy-```.`````  `````   `:oo+/:/oshhhyyyoo/.              
             ``   osyhhyo.         -oos. ```/ys/`..-://+hhdddysyyhs//++:-.`         `:oyo-    .shhhhyy/                 
          `.:+::-:sshhhs-           -syy+.`.oyyyooooysssyhyhhyyyyyhhoossyoo/:-   `./oss/`      .syhdhhy.`.::`           
           -+/oosyshhhs/             .oyhhsoso+sos/+ooooshysohhssyo//yhyyo/+/+///+oos+.         -syhdhhss/o+/-`         
             ---oyyhdys`              `+hyoyhs+oo++oyoshoss/+ss++/-/sss+-//+oo/ossyo:`           +shhdhhyss+:           
                ssyyhy/             `-/ososoososo/:.  .+sss//oo/o+oo.`.`    .-/+o/-`             .syhdyhs```            
           .-..-ysosyy:          `:+sso:../+/:--`    `-os+---+oyyyy:`````                         +sdhhhh.````          
         `:o/ooyyyhyyyy.       .+ss+-`            `:oyhysosydddhyyyooooooo/.                      :shhhhho/+o/.`        
         `.//++oyhdhyyys-     -ss/`            `:+yyss+/:+yhhhhysyy:` `-:oyyo-                    .shhhhhhsso+.         
             ` +syhdhy+sso:..:yy:            `+oso/-.     /yyhho-/ys+/-   .+yso:`                 .yyhhhh+.:`           
               /yyhdyo `-/osso/.            `oo/-        `+syhhy+-sh+syo.   .yhys+:-`             .syhhhh/              
          `:///syyhhhs`                    -oo:          -yhyyyhyyhyssshy.   `shshysss+::--.`     -yhhhhh:-/-`          
         `-oooosyyyhhs-                   /s-.           :yhhhhhyssssoosys    `oyo/:/+osoossso/`  /shhhyhs+oos-`        
           ..:. syyhhy/                   .o          `.-::/ss+shhdhhhhshy:     -sso+/:-``.-/syy+.syhhhyo/+s+.          
                :yyhdhs`                           `-/oo+oooooo+o+ooosssy+        ./osyyys/`  /yyyydhhhy-  `            
             .///hyyhhy+                 `--://::/+oo++++ossyyo+::/+++/+/`            `-+yys-  /hhyhdhyy-::             
            .oooohyyhhhy:           `:/osyyhhyssoo+++ohddddmmhy:   `                     .yyy: `hhhdhyhyooos.           
            .///+.+syhdhy-           osoyyyyo+-`    .ydhoydhys+`                          `yys:/sddhyy:/+o+..           
                   oyyhhhs-          `//+/-`       `ohy/yyso-                              -yyyyhdhyy/                  
                `::+hyyyhhy:                       /syoooo:`                               .hhhhhhyyo::-                
                /soossyyyhhh+`                    -osyo/o-                                 .yhhhhyyhsoos.               
               .:+++:`/yyyhhhs-                   `+o+//ss:                               :syhhhys-.+/o:-               
                      `/hyyshhh+.                   -sooyyyo`                           -+yyyhyyo.                      
                    `+ooohyysyhhy+.                  .ssssss+                         -/syhhyyyy+++`                    
                    .osss/-oysoyhh+/:`                .sys+os`                     `:oyhhhyys/oysss.                    
                    ``-`.  `:sysssss+++:.              `/yoos:                  .-/oyyhhyss/. `:.:`.                    
                           :+syhysss/://oo:.`            :yssy.             .-/osyoshyyyyhso/`                          
                          `+sss+./syyo+:+/sso+/-.`     `-/o+ysy/`      `.-/oossyyhyyss+-oysys.                          
                           :.:-`  `./oyso//++hhysso////oysyhhhhh:--./oosssssyssyyyy+:`  .-///`                          
                                     `.:+oyyydyoyyyshmhyhdhhhdhyyhhyhyhyyyyysoys+:`                                     
                                         `/smdyyysyhdmdhhys:o+syhyshhyshhdhs+://                                        
                                           -hmdmddddmddmyosyhsyhds/yhyyhhy+/-                                           
                                          -+dhddhysyhddyyhmmmddmNho+hyhdhdhhy-                                          
                                         .syyyhdddddhhddmmmmmdddmmdhddddddyyys`                                         
                                          :syyyhhyyydhysshhhsysyhyyyyssshhyhs:                                          
                                     `:::://sddmdhhhmhhosdhhoohdyyyhmhyhdmdh+::::-                                      
                                     -++sysosdmmmmmmmmmddmmmdddmddddmmmddmmhysso++`                                     
                                     /oyhyyyyhdddddddddddddddddddddhhhhdddddhhhdyo:                                     
                                    ./+yhhyhhhyhhhhhhhhhhhhhyyyssssyyysyhddhdddhso+`                                    
                                   `/+++oshddddhdhhhhhysshhyhs+//s:so//hhmmddyso++++`                                   
                                   :oooooosyhhhdhhhhhhyyyyhhhyoosysyyssyhhhhsooooo+o/                                   
                                  `+oyddddddddhhhhhhhhhdhhhhhhhhhhhyhhyyhyhyhhhhhhyoo`                                  
                                  :ooyhhhhhhhhhhhhhhhhyhyyyyhyhyyhhyyyssyyyyhhyhyysoo:                                  
                                 `ooshhhhhhhhhddddddhhyyyyyyyyyyyyyyyyyysssssyyyyyyooo                                  
                                 /ssyyyyysysyhhyyysoo+s+++/////:+/o/::-::--//-+//////s-                                 
                                .yhhhhhhhhhhhhyhyyyyyyysssssssssysysooo+oooososooooooo+`                                
                               `-+++oooooooooooooooooooo++++++++++++++++++++++++++++///.`                               
                                ``...................................................```                                
                                                                                                                        
"""

logo_0_80 = """
                                                                                
                                       `:`                                      
                                 .-`  .oo+`  `.-                                
                           `:-` `/++  `oo+   +o+.  `.-                          
                      ..`  :++:.-+yo/++so+/::+o+.``+++`  ``                     
                     `/+/..:syyyyyyyyyhhyyyysoo++//oo-` :++.                    
                `--.  -syyyyyyhyssoo+syyyys+++ossysso+/:s+:` `..                
                 /++:/syyyyso/:-..`  /hyyyy:  `-:/+ssyys+o/.-+++`               
             ... `/yyyhys+-..`.``.` `-ososs:   ``.-.:+ooyysoos/. ``             
             /+o/+syhy+-` .`.```````/sosssso- ````````-:-+syyso--///            
              .osyhy+.   -.``..````-/+oso+ss:````````  `` .+yhssss/-            
         `::/.+syhs-    `/:.`.`.```.oyososyso.````` ````.   :++sys.`--`         
          :/osshho`     /oo+`.`.`...-sssoyss-```````` ``` ./++ohdyyo+o:         
         ` `+shho`     .os-``-o/`.-::sddhyhy/:/:.`      `/o/.`.ohhhy/.          
       .//:/shhs`       -sy/-+ssooososhyyysyyosys+/:``./oo-    `ohhhs-:/.`      
        -:/yyhy:         .shsysoo/osysyooyo+:oso///++oso:`      .shdhyo+:`      
        ` -ssys`       `:+++oo+o/-` -so/:ooos-``  `.:/-`         +hhhy``        
      `///syyyy-     :+o:.  `.`` `-+yy+oyhyyy////:`              -ydhh/:/.      
      `-::oyhhys:` `+s-        -/os+:-/yhhsss-`.-+s/.            `yhhhso/.      
          oshy+-/o+o+.       `/+:`    .syhs:yos/` .sy+:.`        `shhh-         
       :/+yyhh+             .+/`      /hhyhsysoys` `oyyoso/:::.  .yhhh:/:`      
      `-:::yyhs`            /-      `./+ssyhhhysh/   :so//:-:+yo-/yhhsoo+.      
         ``syhh:              .``.-/ooosso+/++oss`     -/+ss/``ohyhhy:``        
        -ooyyhhy.       `-:+sysoo+++syhhdy:`.-.`           -ys.`hhhyyoo+`       
        `::./yhhs`      .ssyo/:`  `shsyyo:                  -ys/ydhs-:/.`       
           .-yyhhs.       ``      /yooo-                     shhhhy/-           
          .ooooyyhy:             .os+o-                     .shhhssos:          
           ````/yyyho.            .o+sy+`                 `:syhyo```.           
             `oossysyy+.           `osss:               `:oyhysyoo`             
             `-:-`-sssso+:-`        `/soo            `-/shhys:`//:.             
                  /oyoss+//+/-.       +os+`      `-:+syshyohso`                 
                  :/:``:+so+++ys+/--:osshhs..-/+oosssyyo/.`/++                  
                         `-/shhsyyymhhhsyyyyyyyyyyyos/.`                        
                            .yddhhdddhosssdyohyyhs/.`                           
                            /yhddyhhdydmmdmdshhddhh/                            
                           `+syhhyhhyhdhyyhhyhysdyy+                            
                         :/++odmmhddhyddshdhhdhhddy//:-                         
                        `+yysyddddddddddddddddddddhhhy+                         
                        -+syhhhhhhhhyyhhysososoyhddhhs+:                        
                       .+oooyhddhhhhyyhhho+soyoyhdhsoooo.                       
                       /ohdhdhhhhhhhhhhhhhhhyyyyyyyhhhyo+                       
                      .oshhhhhhhhhhhyyyyyyyyyyyssssyyyyso.                      
                      oyhyyyyyhyyyssso+++++oo+///://o///+/                      
                     .osssssssoooooooooooooooooo++oooooo+/`                     
                      `````..........```........``````````                      
"""

logo_1_80 = """
                                     -+`                                        
                                    .-ho                                        
                               .::` `+ho.                                       
                                 /. :shdy/`                                     
                             `/::  `:/yddd+`                                    
                               .. `./:-:-`hy`                                   
                               `+:--/s/syhddo                                   
                               `-:``.+:-+hydh                                   
                               `+o`:o.os+osds                                   
                               .-`   .ydddddy                                   
                               .:o/ ``sddddddy/`                                
                               :sys  `/o/sddddd/                                
                            .+.`/d+     /dddys:                                 
                           -/:+s.h`     /y./:s.                                 
                           `/.`-:ys/`   `/`. -y- `-oo-                          
                      `.       `/-+sh+/++/::--.:-   hdo                         
                     `.   `-    .`  -/:::-:/  `yy  `hdd.                        
                     ..  .+ds   ```-`    -:-  `hdy:/hdds.                       
                     .-  :ddy`  .. `.:-.`-:. `/ddd+  :hdd-                      
                    ``..`.dddh:. `...`.-.`/.-odddd..-:/dds                      
                    .//::hdhd.   .`   .:  +  .dddh````.ddy                      
                       `sdo`y:    .-     ::  :dddh    +ddh`                     
                     `:hh-  .h-    `..-/--   +ddd:     /ddy`                    
                     `hd/    .s:      .+     sddy       `-+y                    
                     .ds     /o`      `-     .odd-         ..                   
                    `sy`    :d:        :      oddd:      `..-`                  
               `-..`+:     :ddh+.          `:oydhhy ` ``.`-..`/`                
              `--`-s`.:-::/hd+-...   `-::::--:/.`/oy+yh+`-  ``:.                
              `..  o`  ``.:+s/-.         -::-.::`./--/`  ````-/+                
             `-````/ `.-:+oyysoo/`     `//+shy-  ..       `.../.                
             .`..```        .+hddyoossyso//--+`          -o::/.                 
             `.``.`       `..`:--..``               `-+shddy`                   
               `` `.`  ``..-----::://:-.       `-/oyddho+:.                     
                    `-/-:------....`      `-/oyddddddd.                         
                     :s--     -::--:/+++/:::--. .:osys/                         
                      ::.     `                                                 
                                                                                
                                                                                
"""

logo_2_80 = """
                                       .                                        
                                     -NMd`                                      
                                     hMMMo                                      
                                     NMMMy                                      
                                    -MMMMh                                      
                                    yMMMMM+                                     
                                    /MMMMm:                                     
                   `yh`              yMMN-`                                     
                   `NMN.       -+shdNMMMMMMNhs/`          .s:                   
                   .M.       +mMMMMMMMMMMMMMMMMm:      `:omN:                   
                   -mNds:`-yNMMNydMMMMMMMMMNsyNMMh- `/smshMNo`                  
                   :NmhNMMMMms:-mMMMMMMMMMMMMd./hMMmMMNyss``                    
                  `oNMdymy+- .yMMMh+mMMMMMohMMMs`.yMMdsdMm/                     
                   `.`  .sNNhMMm+`  /MMMMMm-`+mMNNMd/   ``                      
                          `ods- .+hNMMMMMMMN.  -ss-                             
                             :yNMMMdhMMMMMMMy                                   
                        ..:yNMMmy+..hMMMMMMMh                                   
                    /mmNMMNs+-`   -NMMMMm:-.                                    
                     .:-..`      :NMMMMh.                                       
                                :NMMMy.                                         
                               -NMMh-                                           
                               oMMN:                                            
                                sMMM/                                           
                                 oMMMo                                          
                                  :mMMo                                         
                                   `oMMo                                        
                                  .++hmNy                                       
                                   ``                                           
                                                                                
"""


def logo():
    logos = (logo_0_80, logo_1_80, logo_2_80)
    return logos[random.randint(0, len(logos) - 1)]
