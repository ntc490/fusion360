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
