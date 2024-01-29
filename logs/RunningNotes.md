#### SEU ECON-D testing Jan 27, 2024

Dump of Jon's notes during data-taking (dumped from google doc)

### Friday afternoon, at FNAL
On hexa42, tests will be run in directory `/home/HGCAL_dev/SEU_test_Jan272024`.
On hexa43, tests will be run in directory `/home/HGCAL_dev/SEU_test_Jan272024`.

Chips 603 and 604 will go to the test.  We will note which chip is connected to which hexacontroller after we set up tonight.

### Friday evening, at cancer center

Front chip is 604
Front means closer to snout
604 black and white power leads
604 top ps, address 6

Back chip is 603
Centered/aligned on back chip
Bottom ps address 8
Orange and purple power leads

Front chip (604) is connected to hexa42
Back chip (603) is connected to hexa43

We have network access to the hexacontrollers and the GPIB as of 7:10pm

Hexacontrollers date/time set themselves automatically

RAMdisks were mounted automatically at boot

Checking on ECON supply voltages: 7:13pm

Both hexacontrollers have `econ-d-tester-socket` firmware loaded, git hash `972710d`.

Running tests at 7:18pm: Grace on hexa43, Danny on hexa42

Hexa42 seems happy, hexa43 not happy yet (7:19)

Running test_bench/test_io.py on hexa42 and hexa43 (7:21)
Hexa42 output (chip 604)
```
array([[255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   3],
       [255, 255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0],
       [255, 255, 255, 255, 255, 225,  88,   0,   0,   0,   0,   0],
       [  2,   0,   0,   0, 255, 255, 255,  47, 255,   0,   0,   0],
       [  0,   0,   0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
       [  0,   0,   0,   0,   0,   6,  48, 255, 255, 255, 255, 164],
       [  0,   0,   0,   0,   0,   0,   0,   2,   0, 255, 255, 255],
       [  0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255],
       [255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,  14],
       [255, 255, 255, 255,  10,   0,   0,   0,   0,   0,   0,   0],
       [255, 206, 255, 182, 255, 255, 255,   0,   0,   0,   0,   0],
       [  0,   0,   0,   0, 255, 255, 255,  55, 255,   0,   0,   0],
       [  0,   0,   0,   0,   0, 255, 255, 255, 255,   0,   0,   0],
       [  0,   0,   0,   0,   0,   0,   0, 255, 255, 255, 199,  10],
       [  0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255]])
```

Hexa43 output (chip 603)

```
array([[255, 255, 255, 255,   1,   0,   0,   0,   0,   0,   0,   0],
   	[255, 255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0],
   	[255,   0, 255,   2, 255, 255, 255,   0,   5,   0,   0,   0],
   	[  0,   0,   0,   0, 255, 255, 255, 255, 255,   0,   0,   0],
   	[  0,   0,   0,   0,   0, 255, 255, 255, 255,   3,   0,   0],
   	[  0,   0,   0,   0,   0,   0,   0, 255, 221, 255, 255, 255],
   	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255],
   	[  0, 255,   0,  86,   0,   0,   0,   0,   0, 255, 255, 255],
   	[255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0],
   	[255, 255, 255, 255, 255,   0,   0,   0,   0,   0,   0,   0],
   	[255,   0,   0,   0, 255, 255, 255,   0,  14,   0,   0,   0],
   	[  0,   0,   0,   0, 255, 255, 255, 255, 255,   0,   0,   0],
   	[  0,   0,   0,   0,   0, 255,   5, 255, 255,   0,   0,  93],
   	[  0,   0,   0,   0,   0,   0,   0, 255,  72, 255, 255, 255],
   	[  0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255, 255]])
```

We think the reason hexa43 was not happy was because the phases were tuned for chip 603 on hexa42 and chip 604 on hexa43 - we have swapped them, and needed to do new phase scans to find the correct phase settings


From above phase scans, find best phase_select settings (from weighted 5 wide window)
`[5, 5, 5, 5, 6, 7, 7, 8, 8, 2, 2, 2]`
`[ 5,  4,  5, 12,  6,  7,  7,  8,  8, 10,  2,  2]`
We changed the settings by hand to try and get 43 more stable, but it did not work (or it was marginal). We will put more 68 uF more on. `[5, 12, 5, 12, 6, 7, 7, 8, 7, 10, 2, 2]`

Committed these changes to git and pushed from hexa42.  Changes pulled on hexa43.


Power supplies - we tuned so the chips have 1.2 V at the boards, to account for the drop across the wires. The new voltage settings and draws:


Saw “Format code” errors during PRBS test.  This was because force_ch_output was getting set *after* PRBS input was already turned on, so some PRBS data was going through the ECON and causing format code errors.  Solution is to turn force_ch_output on first, and then turn on PRBS input.

Added 68 μF of capacitance to chip 603 power supply pins.  This seems to have fixed the input CRC errors on chip 603. (hexacontroller 43).  (8:28pm)

### Saturday morning
Set up power strip on hallway table, plugged in laptops.

Powered on hexacontrollers

Connected to hexacontrollers

Internet access for hexacontrollers is Staworking

hexacontroller date and time set automatically

Started logging of `journalctl -f` and `dmesg -w` from both hexacontrollers on Jon’s laptop, in the directory `~jsw/SEU_logs`.

Loaded firmware on both hexacontrollers:
42: 
econ-d-tester-socket.bit
972710d
43:
econ-d-tester-socket.bit
972710d

ECONs powered (8:35am)

Confirmed RAM disks are mounted on both hexacontrollers (8:36am)

Grace committed and pushed changes to phase select.

Tagged the current test code as `SEU_test_Jan2024_v2`.  This is commit 4a5bc442394d760bf86b023319d6b652d638ca06.
Tests before beam

Danny on hexa42

Grace on hexa43

Starting normal SEU test scripts at 8:42 on both hexacontrollers.

normal SEU test scripts succeeded.

Starting PRBS SEU test scripts at 8:44 on both hexacontrollers.

PRBS SEU test scripts succeeded.

Run `test_bench` on both hexacontrollers starting at 8:45.

test_bench successful.

#### Dry run
Start scripts at 8:59:21am
Ready for “beam” at 8:59:42am
21 seconds from start to “ready for beam”
#### Last walkthrough
Re-aligned table with chips, because the table got moved very slightly since last night.
Moved table upwards about 4mm.

Doors closed at 9:13am

#### Another dry run
Start normal SEU test at 9:21:17am
stop at 9:23:41am
#### First beam
Plan for the first beam is 1e10, 15 to 30 seconds. 10 nA current.

Beam is bunched: 50 Hz bunch rate, with 10 ms bunch duration, so the duty cycle is 50%

Start scripts at 9:26:50am
Start beam at 9:27:19am
Stop beam at 9:27:28am
script stopped at 9:27:35am

Flux 1.6e9
300 MU delivered

Counted some TMR errors.
Saw one bit flip before the formatter (so CRC changed), and one bit flip after the formatter (CRC unchanged)

#### Second beam
Plan is for ~30 seconds.  Current 10 nA.

Start scripts at 9:34:53am.

Start beam at 9:35:21am
Stop beam at 9:35:29am
Sop scripts at 9:35:35am

332 MU delivered
#### Third beam
Plan is 1e11, 10 nA, 65s

Scripts start at 9:55:12am
Beam start at 9:55:52am
Beam stop at 9:56:48am
Script stop at 9:57:06am

2708 MU delivered

Some data errors recorded, and TMR errors counted
#### Interlude
Run 104 SEU script start at 10:00:29am, with no beam
No errors recorded yet, so probably the errors we’ve seen are genuinely caused by the beam
stop at 10:05:00am
No errors recorded.
#### Fourth beam
Plan is 112s, 1e12, 50 nA

Scripts start at 10:12:33am
Beam start at 10:13:13am
Beam stop at 10:13:58am
Script stop at 10:14:11am

~44 second beam time, beam aborted because of RF spark
12753 MU delivered
#### Fifth beam
Plan is 85s, 50 nA

Scripts start at 10:19:27am
Beam start at 10:20:04am
Beam stop at 10:20:27am
Script stop at 10:20:37am

23 second beam time
6423 MU
#### Sixth beam
Plan is 85s, 50nA

scripts start at 10:26:19am
beam start at 10:26:46am
beam stop at 10:27:53am
script stop at 10:28:00am

Grace saw a jump by ~30 stream compare errors.  Look for a change in zero suppression that would shift the remainder of the packet by a word.
#### Seventh beam
50nA

script start at 10:38:04am
beam start at 10:38:31am
beam stop at 10:40:00am
script stop at 10:40:11am
#### Eighth beam
Stay at 50 nA, 180s

script start at 10:44:28am
beam start at 10:45:01am
beam stop at 10:48:09am
script stop at 10:48:19am
#### Ninth beam
50 nA, 180s

script start at 10:56:55am
beam start at 10:57:22am
beam stop at 11:00:32am
script stop at 11:00:40am
#### Interlude
Run 999 is a test run, to test the change in capture length from 8 BX to 5 BX
Tenth beam
50 nA, 280s

Reducing capture length from 8 BX to 5 BX

script start at 11:08:57am
beam start at 11:09:26am
beam stop at 11:14:06am
script stop at 11:14:16am
#### Eleventh beam
50 nA, to 4e12, ~380s

script start at 11:25:12am
beam start at 11:25:39am
beam stop at 11:31:49am
script stop at 11:31:57am
#### Twelfth beam
50 nA, to 4e12, ~380s

script start at 11:40:20am
beam start at 11:40:48am
beam stop at 11:46:53am
script stop at 11:47:00am
#### Thirteenth beam
50 nA, to 4e12, ~380s

script start at 11:55:18am
beam start at 11:55:48am
beam stop at 11:59:22am
script stop at 11:59:30am
#### Fourteenth beam
50 nA, ~380s

script start at 12:10:52pm
prebeam errors on hexa42, trying again
script stop at 12:11:45pm

script start at 12:12:03pm
prebeam: started with 3 error counts on hexa42
scrip stop at 12:13:05pm

script start at 12:13:10pm
beam start at 12:13:38pm
beam stop at 12:19:45pm
script stop at 12:19:55pm
#### Fifteenth beam
100 nA, to 4e12, ~190s

script start at 12:27:20pm
beam start at 12:28:18pm
beam stop at 12:31:10pm
script stop at 12:31:17pm
#### Sixteenth beam
100 nA, to 4e12, ~190s

script start at 12:55:13pm
issues on hexa42: picked up a CRC error in prebeam, probably caused by power sag at start up
script stop at 12:55:45

script start at 12:56:04pm
No beam.  Waiting for ETROC script to time out before trying again.
beam start at 12:59:46pm
beam stop at 1:02:45pm
script stop at 1:02:50pm
#### Seventeenth beam
PRBS run

100 nA, to 4e12, ~190s

script start at 1:09:22pm
beam start at 1:10:05pm
beam stop at 1:13:04pm
script stop at 1:13:23pm
#### Eighteenth beam
PRBS run
100 nA, to 4e12, ~190s

script start at 1:17:25pm
beam start at 1:17:54pm
beam stop at 1:20:55pm
script stop at 1:21:05pm
#### Nineteenth beam
PRBS run
100 nA, to 4e12, ~190s

script start at 1:24:48pm
beam start at 1:25:29pm
beam stop at 1:28:27pm
script stop at 1:28:36pm
#### Twentieth beam
ZS Zeroes
100 nA, 1e12, ~60s

script start at 1:36:17pm
Pre-beam errors on hexa42
script stop at 1:36:

script start at 1:37:07pm
beam start at 1:37:37pm
beam stop at 1:38:22pm
script stop at 1:38:30pm
#### Twenty-first beam
ZS Ones
100 nA, 1e12, ~60s

script start at 1:44:44pm
beam start at 1:45:53pm
beam stop at 1:46:38pm
script stop at 1:46:45pm
#### Twenty-second beam
PRBS
100 nA, 1e12, ~60s

script start at 1:50:38pm
beam start at 1:51:09pm
beam stop at 1:51:48pm
script stop at 1:51:58pm
#### Post beam
Run test_bench at 1:55:49
Some test_bench failures on hexa43
Crashed on hexa42
Running again

hexa42 filesystem flipped to read only at about 11:15am.

Start run 23 (normal SEU script) at 2:12:28pm