import sys
sys.path.append("/home/mnikonov/.local/lib/python3.5/site-packages")

from datalist import *
from plumbum import local
from itertools import zip_longest
import os

def show_usage():
    print("MadTester v0.1")
    print("Usage: MadTester DATA_LIST [OUTPUT_DIR]")

def check_args(args):
    if not 1 < len(args) < 4:
        show_usage()
        exit()

def createdirs(pathdir):
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)

def test(experement, output_dir):
    createdirs(output_dir)
    kvals = [55, 61]
    for k in kvals:
        run_experenet(experement, k, output_dir + "/" + experement.name + "_" + str(k))

def run_rnaSPAdes(experement, k, output_dir):
    print("~ running SPAdes on " + experement.name);
    rnaspades = local["rnaspades.py"]
    args = ["-k", k, "-o", output_dir]
    for r1, r2 in zip_longest(experement.r1, experement.r2):
        args.extend(["-1", r1, "-2", r2])
    rnaspades(args)
    print("~ SPAdes successfully finished work")

def run_rnaQUAST(experement, output_dir):
    print("~ running rnaQUASt")
    rnaQUAST = local["rnaQUAST.py"]
    rnaQUAST["-r", experement.ref, "--gtf", experement.gtf, 
            "-c", output_dir + "/transcripts.fasta", "-o", output_dir]()
    print("~ finished rnaQUAST")

def remove_tmpdata(output_dir):
    pass

def run_experenet(experement, k, output_dir):
    if "madTester" not in output_dir:
        raise RuntimeError("Bad output_dir: " + output_dir)
    rmcmd = local["rm"]
    rmcmd["-rf", output_dir]()
    createdirs(output_dir)
    print("Evaluating experement " + experement.name + " with k-mer size = " + str(k))
    run_rnaSPAdes(experement, k, output_dir)
    run_rnaQUAST(experement, output_dir)
    remove_tmpdata(output_dir)
    print("Done!") 
    

def main(args):
    check_args(args)
    output_dir = "results" if len(args) < 3 else args[2]
    output_dir += "/madTester" # protection form accidental deletion of unrelated data
    try:
        mad_data = TestData(args[1])
        for exp in mad_data.experements:
            test(exp, output_dir)
    except DataListExc as datalist_exception:
        print("Invalide DATA_LIST format!")
        print(datalist_exception)

if __name__ == '__main__':
    main(sys.argv)


