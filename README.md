# Getting the Leela Ratio on your machine

First off, this ratio is intended as a rough measure of gpu vs cpu performance. It is based on the ratio
of nodes per seconds (nps) reported for A0 vs Stockfish 8, which had SF8 searching 875 times as many nodes
as A0.

So our ratio is lc0 nps * 875/ sf9 nps. Why Stockfish 9? Because more people have it than Stockfish 8.
Also, they search roughly the same number of nodes. Roughly.

If you're planning on running Ethereal with 4 threads and 1GB hash, then you should compute the Leela
Ratio with the same parameters for Stockfish.

## Monster Machines

If you have a truly monster machine for either CPU or GPU, you may want to increase the depth or nodes in the YAML file,
respectively to get a more consistent measurement.

## Running the Tool

```
$ python ratio.py 
Running stockfish to depth 27.
5737993 nps
   T
 .-"-.
|  ___|
| (./.)
|  ,,,' 
| '###
 '----'
Bender (based on lc0) 0.18.1 built Oct  3 2018
Loading weights file from: /home/dkappe/work/chess/Arena/Engines/LeelaZero/192/weights_11258.txt.gz
Creating backend [cudnn]...
Running leela to 200000 nodes.
5363 nps

===
GPU:                 GTX 1070
Stockfish threads:   4
Stockfish hash:      1024
Stockfish depth:     27
Stockfish nps:       5737993
Leela threads:       2
Leela nodes:         200000
Leela nps:           5363
Leela Ratio:         0.818
Leelafish Ratio:     1.914
===
```