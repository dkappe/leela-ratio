import chess
import chess.uci
import yaml
import os.path

# Load some external config file
with open('ratio.yaml') as fp:
    conf = yaml.load(fp)

# test conf
stockfish = conf["stockfish"]["cmd"]
if not os.path.isfile(stockfish):
    print("Stockfish command {} doesn't exist.".format(stockfish))
    exit(1)

if conf["stockfish"]["threads"] == None:
    sf_threads = 1
else:
    sf_threads = conf["stockfish"]["threads"]

if conf["stockfish"]["hash"] == None:
    sf_hash = 1024
else:
    sf_hash = conf["stockfish"]["hash"]

if conf["stockfish"]["depth"] == None:
    sf_depth = 28
else:
    sf_depth = conf["stockfish"]["depth"]


# leela
leela = conf["leela"]["cmd"]

if not os.path.isfile(leela):
    print("Leela command {} doesn't exist.".format(leela))
    exit(1)

if conf["leela"]["threads"] == None:
    leela_threads = 1
else:
    leela_threads = conf["leela"]["threads"]

if conf["leela"]["weights"] == None:
    print("Leela weights file not defined.")
    exit(1)

leela_weights = conf["leela"]["weights"]

if not os.path.isfile(leela_weights):
    print("Leela weights file {} doesn't exist.".format(leela_weights))
    exit(1)

if conf["leela"]["nodes"] == None:
    leela_nodes = 200000
else:
    leela_nodes = conf["leela"]["nodes"]

# get the sf nps

sf = chess.uci.popen_engine(stockfish)
sf_conf = {'Threads' : sf_threads, 'Hash' : sf_hash }
sf.setoption(sf_conf)
sf.isready()

sf_info = chess.uci.InfoHandler()

sf.info_handlers.append(sf_info)

print("Running stockfish to depth {}.".format(sf_depth))
sf.go(depth=sf_depth)

sf_nps = sf_info.info['nps']


print("{} nps".format(sf_nps))

# get the leela nps

lc = chess.uci.popen_engine(leela)
lc_conf = {"Network weights file path" : leela_weights, "Number of worker threads" : leela_threads}
lc.setoption(lc_conf)
lc.isready()

lc_info = chess.uci.InfoHandler()

lc.info_handlers.append(lc_info)

print("Running leela to {} nodes.".format(leela_nodes))
lc.go(nodes=leela_nodes)

lc_nps = lc_info.info['nps']

print("{} nps".format(lc_nps))

# compute leela ratio

ratio = 875.0 * lc_nps / sf_nps

print("\n===")
print("GPU:\t{}".format(conf["gpu"]))
print("Stockfish threads:\t{}".format(sf_threads))
print("Stockfish hash:\t{}".format(sf_hash))
print("Stockfish depth:\t{}".format(sf_depth))
print("Stockfish nps: {}".format(sf_nps))
print("Leela threads:\t{}".format(leela_threads))
print("Leela nodes:\t{}".format(leela_nodes))
print("Leela nps: {}".format(lc_nps))
print("Leela Ratio:\t{}".format(round(ratio,3)))
print("===")

# clean up
lc.quit()
sf.quit()
