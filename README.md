# fusion360
## Convert Fusion360 Tool Library to LinuxCNC Tool Table

### Script Usage

	ttable.py, Copyright (C) 2016 Nathan Crapo
	ttable.py comes with ABSOLUTELY NO WARRANTY; for details
	see GPLv2 header within.  This is free software, and you
	are welcome to redistribute it under certain conditions;
	see header for details.

	Usage:
	  ttable.py [-o <output_file>] [-m | --metric]  <file>
	  ttable.py [-o <output_file>] [-i | --imperial] <file>

	Options:
	  -m, --metric                 Set machine units to metric (default)
	  -i, --imperial               Set machine units to imperial
	  -o <file>, --output <file>   Specify an output file (defaults to stdout)
	  --version                    Print program version


	ttablev2.py, Copyright (C) 2016 Nathan Crapo
	ttablev2.py comes with ABSOLUTELY NO WARRANTY; for details
	see GPLv2 header within.  This is free software, and you
	are welcome to redistribute it under certain conditions;
	see header for details.
	
	Usage:
	  ttablev2.py [-o <output_file>] [-m | --metric] [-l | --linuxcnc-file <linuxcnc-file-name> ]  <file>
	  ttablev2.py [-o <output_file>] [-i | --imperial] [-l | --linuxcnc-file <linuxcnc-file-name>] <file>
	
	Options:
	  -m, --metric                        Set machine units to metric (default)
	  -i, --imperial                      Set machine units to imperial
	  -l <file>, --linuxcnc-file <file>   Merge data with existing linuxcnc_file
	  -o <file>, --output <file>          Specify an output file (defaults to stdout)
	  --version                            Print program version

### HOWTO

#### In Fusion360

1. Select the CAM workspace
2. Select "Manage" dropdown list
3. Select "Tool Library" menu item to produce "CAM Tool Library" dialog
4. Right click a library in the left pane of the dialog and select "Export Tool Library"
5. Specify a file


#### From the console of your computer

Use the ttable.py script to convert your exported tool library to a Linux CNC
tool table.

Here's an example invocation:

	[ncrapo@oahu] fusion360% ./ttable.py export-8-24-18.tools
	t1 p1 z0 d3.175000 ;Inventables - 2 Flute Straight
	t2 p2 z0 d1.587500 ;Inventables - Upcut Fish Tail Spiral
	t3 p3 z0 d3.175000 ;Inventables - Solid Carbide Ball
	t4 p4 z0 d3.175000 ;Inventables - Single Flute Upcut
	t5 p5 z0 d3.175000 ;YooCNC - Spiral Upcut
	t6 p6 z0 d1.587500 ;Kyocera - Single flute upcut for plastic [acrylic and polycarbonate]
	t7 p7 z0 d3.175000 ;Kyocera - 2 Flute Upcut for plastic, AL, soft media, wood, or copper
	t8 p8 z0 d3.175000 ;Onsrud - 1 Flute Upcut for plastic
	t9 p9 z0 d3.175000 ;Inventables - 30 Degree V-Bit
	t10 p10 z0 d3.175000 ;Fullerton - 90 Degree V-Bit
	t11 p11 z0 d1.587500 ;DJTOL N - Single flute upcut spiral
	t12 p12 z0 d0.793750 ;Inventables - Fishtail 2 flute upcut
	t13 p13 z0 d3.175000 ;Kyocera - Stub Ball
	t21 p21 z0 d3.175000 ;Inventables 30388-01 - 30 Degree x 0.1 V-Bit
	t22 p22 z0 d3.175000 ;Inventables 30388-01 - 25 Degree x 0.1 V-Bit
	t23 p23 z0 d3.175000 ;Inventables 30388-01 - 20 Degree x 0.2 V-Bit
	t24 p24 z0 d3.175000 ;Inventables 30388-01 - 20 Degree x 0.1 V-Bit
	t25 p25 z0 d3.175000 ;Inventables 30388-01 - 15 Degree x 0.2 V-Bit
	t26 p26 z0 d3.175000 ;Inventables 30388-01 - 15 Degree x 0.1 V-Bit
	t27 p27 z0 d3.175000 ;Inventables 30388-01 - 10 Degree x 0.2 V-Bit
	t28 p28 z0 d3.175000 ;Inventables 30388-01 - 10 Degree x 0.1 V-Bit
	t29 p29 z0 d3.175000 ;Inventables 30388-01 - 5 Degree x 0.2 V-Bit
	t30 p30 z0 d6.000000 ;YooCNC - Spiral upcut for AL
	t31 p31 z0 d12.700000 ;Skil - Straight Router Bit
	t32 p32 z0 d3.175000 ;Oliver Tool Company - Long reach upcut for plastic, soft media, or wood
	t33 p33 z0 d3.175000 ;Kyocera - Spiral Upcut fishtail for plastic or wood
	t34 p34 z0 d6.350000 ;Fullerton - 90 Degree V-Bit
	t35 p35 z0 d6.350000 ;Inventables / Onsrud - Straight flute for hard and soft plastics
	t36 p36 z0 d6.350000 ;Inventables / Onsrud - Single flute upcut spiral for fiberglass, phenolic, and aluminum
	t37 p37 z0 d6.350000 ;Inventables / Onsrud - Engraving bit for wood, plastic, and aluminum
	t38 p38 z0 d12.700000 ;Skil - Router bit
	t39 p39 z0 d6.350000 ;Onsrud - Single flute for plastic
	t40 p40 z0 d1.400000 ;Kyocera - DIAMOND CUT CARBIDE ROUTER BURRS
	t41 p41 z0 d3.175000 ;Kyocera - DIAMOND CUT CARBIDE ROUTER BURR
	t101 p101 z0 d0.300000 ;Inventables - PCB drill
	t102 p102 z0 d0.400000 ;Inventables - PCB drill
	t103 p103 z0 d0.500000 ;Inventables - PCB drill
	t104 p104 z0 d0.600000 ;Inventables - PCB drill
	t105 p105 z0 d0.700000 ;Inventables - PCB drill
	t106 p106 z0 d0.800000 ;Inventables - PCB drill
	t107 p107 z0 d0.900000 ;Inventables - PCB drill
	t108 p108 z0 d1.000000 ;Inventables - PCB drill
	t109 p109 z0 d1.100000 ;Inventables - PCB drill
	t110 p110 z0 d1.200000 ;Inventables - PCB drill


        paju@mule:Tool Library$./fusion360/ttablev2.py --metric --linuxcnc-file ./tool.tbl 'F360 SK30 Master v2 20210209.tools.json'
        Tool 276, igoring LinuxCNC diameter and length data due to either I(102.500000/154.500000), J(6.000000/6.000000) or type(16/16) mismatch
	Tool 275, igoring LinuxCNC diameter and length data due to either I(48.500000/114.300000), J(4.000000/4.000000) or type(16/16) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/117.500000), J(3.000000/5.000000) or type(2/2) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/103.200000), J(3.000000/3.000000) or type(2/2) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/106.700000), J(3.000000/6.000000) or type(2/2) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/102.700000), J(3.000000/8.000000) or type(2/2) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/98.700000), J(3.000000/4.000000) or type(2/2) mismatch
	Tool 260, igoring LinuxCNC diameter and length data due to either I(113.000000/106.500000), J(3.000000/10.000000) or type(2/2) mismatch
	Skipping duplicate tool numbers ...
	T10 P0 Z0.000000 D3.000000 I91.400000 J3.000000 Q1  ; - 3 flute End Mill - flat end mill
	T11 P0 Z-57.164400 D3.029500 I96.000000 J3.000000 Q1  ; - 2 flute End Mill - flat end mill
	T12 P0 Z0.000000 D3.000000 I87.000000 J3.000000 Q1  ; - 2 flute End Mill - ball end mill
	T13 P0 Z0.000000 D4.000000 I62.500000 J4.000000 Q1  ; - 4 flute End Mill - flat end mill
	T14 P0 Z0.000000 D6.000000 I63.000000 J6.000000 Q1  ; - flute End Mill - flat end mill
	T15 P0 Z0.000000 D6.000000 I65.000000 J6.000000 Q1  ; - 3 flute End Mill - flat end mill
	T16 P0 Z-77.937000 D6.072100 I77.000000 J6.000000 Q1  ; - 2 flute End Mill - flat end mill
	T17 P0 Z0.000000 D6.000000 I86.000000 J6.000000 Q1  ; - 3 flute End Mill - ball end mill
	T18 P0 Z0.000000 D6.000000 I175.500000 J6.000000 Q1  ; - 2 flute End Mill - ball end mill
	T19 P0 Z0.000000 D6.000000 I130.000000 J6.000000 Q1  ; - Empty - flat end mill
	T20 P0 Z0.000000 D5.000000 I90.500000 J5.000000 Q1  ;Biax - 4 flute End Mill - flat end mill
	T21 P0 Z0.000000 D5.000000 I87.000000 J5.000000 Q1  ; - Empty for Biax - flat end mill
	T22 P0 Z0.000000 D8.000000 I70.000000 J8.000000 Q1  ; - 3 flute End Mill - flat end mill
	T23 P0 Z0.000000 D8.000000 I85.500000 J8.000000 Q1  ;Holex - 4 flute End Mill - flat end mill
	T24 P0 Z0.000000 D8.000000 I78.700000 J8.000000 Q1  ;Holex - 6 flute End Mill - flat end mill
	T25 P0 Z0.000000 D8.000000 I105.500000 J8.000000 Q1  ; - 4 flute End Mill - bull nose end mill
	T26 P0 Z0.000000 D8.000000 I138.300000 J8.000000 Q1  ; - 4 flute End Mill - flat end mill
	T30 P0 Z0.000000 D10.000000 I81.000000 J10.000000 Q1  ; - 4 flute End Mill - flat end mill
	T31 P0 Z0.000000 D10.000000 I83.500000 J10.000000 Q1  ;Holex - 4 flute End Mill - flat end mill
	T32 P0 Z0.000000 D10.000000 I105.500000 J10.000000 Q1  ; - 4 flute End Mill - ball end mill
	T35 P0 Z0.000000 D12.000000 I75.300000 J12.000000 Q1  ; - 3 flute End Mill - flat end mill
	T36 P0 Z0.000000 D12.000000 I93.000000 J12.000000 Q1  ; -  3 flute End Mill *** LEFT HAND *** - flat end mill
	T37 P0 Z-57.234400 D12.062700 I88.000000 J12.000000 Q1  ; - 6 flute End Mill - flat end mill
	T38 P0 Z0.000000 D12.000000 I79.000000 J12.000000 Q1  ; - Empty - flat end mill
	T39 P0 Z0.000000 D12.000000 I79.000000 J12.000000 Q1  ; - Empty - flat end mill
	T45 P0 Z0.000000 D16.000000 I113.500000 J16.000000 Q1  ; - Roughout Flat End Mill - flat end mill
	T46 P0 Z0.000000 D16.000000 I63.800000 J16.000000 Q1  ; - Empty - flat end mill
	T47 P0 Z0.000000 D20.000000 I75.400000 J20.000000 Q1  ; - Empty - flat end mill
	T70 P0 Z0.000000 D20.000000 I79.000000 J20.000000 Q1  ;Iscar - Face Mill - face mill
	T71 P0 Z0.000000 D40.000000 I39.500000 J40.000000 Q1  ; - Empty - face mill
	T72 P0 Z0.000000 D49.800000 I65.700000 J49.800000 Q1  ; - Face Mill - face mill
	T73 P0 Z0.000000 D52.000000 I59.500000 J52.000000 Q1  ; - Face Mill - face mill
	T74 P0 Z0.000000 D52.000000 I49.500000 J52.000000 Q1  ; - Empty - face mill
	T75 P0 Z0.000000 D99.300000 I77.400000 J99.300000 Q1  ; - Face Mill - face mill
	T80 P0 Z-63.521061 D6.039100 I95.500000 J6.000000 Q2  ;Vobeco - 40°Chamfer Mill - chamfer mill
	T81 P0 Z-71.432200 D4.140600 I94.500000 J4.000000 Q2  ; - 60° Chamfer Mill - chamfer mill
	T82 P0 Z-75.123955 D9.857865 I79.500000 J10.000000 Q2  ; - 40° Chamfer Mill - chamfer mill
	T95 P0 Z0.000000 D49.900000 I127.300000 J49.900000 Q1  ; - Slitting Saw 13mm Arbor - slot mill
	T96 P0 Z0.000000 D100.000000 I170.000000 J100.000000 Q1  ; - Slitting Saw 20mm Arbor - slot mill
	T200 P0 Z0.000000 D3.000000 I109.800000 J3.000000 Q2  ; - 2-8mm Drill Chuck - drill
	T201 P0 Z0.000000 D4.000000 I84.000000 J4.000000 Q2  ; - 3.3mm Carbide Drill - drill
	T202 P0 Z0.000000 D4.000000 I84.000000 J4.000000 Q2  ; - 4mm Carbide Drill - drill
	T203 P0 Z-74.469300 D4.252600 I78.000000 J4.000000 Q2  ; - 4.2mm Carbide Drill - drill
	T204 P0 Z0.000000 D5.000000 I94.000000 J5.000000 Q2  ; - 5mm Carbide Drill - drill
	T205 P0 Z-60.356900 D6.000000 I95.000000 J6.000000 Q2  ; - 6mm Carbide Drill - drill
	T206 P0 Z0.000000 D6.000000 I105.500000 J6.000000 Q2  ; - 6.8mm Carbide Drill - drill
	T207 P0 Z-64.573300 D7.262500 I97.500000 J8.000000 Q2  ; - 8mm Carbide Drill - drill
	T208 P0 Z0.000000 D10.000000 I110.500000 J10.000000 Q2  ; - 8.6mm Carbide Drill - drill
	T209 P0 Z0.000000 D14.000000 I131.800000 J14.000000 Q2  ; - 14mm Carbide Drill - drill
	T210 P0 Z0.000000 D15.800000 I138.300000 J15.800000 Q2  ; - 16mm Carbide Drill - drill
	T211 P0 Z0.000000 D3.000000 I150.000000 J3.000000 Q2  ; - 2-16mm Drill Chuck - drill
	T212 P0 Z0.000000 D3.000000 I172.200000 J3.000000 Q2  ; - 2-16mm Drill Chuck - drill
	T213 P0 Z-57.998300 D4.101800 I92.300000 J6.300000 Q2  ; - 2.4/6.3 spot drill 2-8mm Drill Chuck - center drill
	T214 P0 Z0.000000 D12.000000 I94.500000 J12.000000 Q2  ; - spot drill - spot drill
	T260 P0 Z0.000000 D3.000000 I113.000000 J3.000000 Q2  ; - WES 1B - tap right hand
	T261 P0 Z0.000000 D10.000000 I144.000000 J10.000000 Q2  ; - ER20 - tap right hand
	T275 P0 Z0.000000 D0.000000 I114.300000 J4.000000 Q16  ; - Edge Finder - probe
	T276 P0 Z0.000000 D0.000000 I154.500000 J6.000000 Q16  ;Renishaw - MP12H - probe

