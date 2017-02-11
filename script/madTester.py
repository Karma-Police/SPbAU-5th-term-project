import sys
sys.path.append("/home/mnikonov/.local/lib/python3.5/site-packages")

from datalist import *
from summary import *
from plumbum import local
from itertools import zip_longest
import os
import shutil

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

def error_correction(corrected_dir, experement):
    if os.path.isdir(corrected_dir):
        print("Skipping error correction for " + experement.name + " cause it is already done")
        return
    print("~ Performing error correction for " + experement.name);
    rnaspades = local["rnaspades.py"]
    args = ["--only-error-correction", "-o", corrected_dir]
    for r1, r2 in zip_longest(experement.r1, experement.r2):
        args.extend(["-1", r1, "-2", r2])
    rnaspades(args)
    print("~ finished error correction")

def test(experement, output_dir, summary):
    createdirs(output_dir)
    corrected_dir = output_dir + "/_err_" + experement.name;
    error_correction(corrected_dir, experement)
    corrected_yaml = corrected_dir + "/corrected/corrected.yaml";
    if not os.path.isfile(corrected_yaml):
        raise RuntimeError("corrected.yaml file not found")
    kvals = [39, 43, 47, 49, 51, 53, 55, 57, 59, 61, 63, 67, 71]
    for k in kvals:
        experement_dir = output_dir + "/" + experement.name + "_" + str(k);
        run_experenet(experement, k, corrected_yaml, experement_dir)
        print("~~ saving report")
        f = open(experement_dir + "/short_report.txt", "r")
        summary.addrep(experement.name, k, f)
        f.close()
        print("~~ saved")

def run_rnaSPAdes(experement, k, corrected_yaml, output_dir):
    print("~ running SPAdes on " + experement.name);
    rnaspades = local["rnaspades.py"]
    args = ["-k", k, "-o", output_dir, "--dataset", corrected_yaml]
    rnaspades(args)
    print("~ SPAdes successfully finished work")

def run_rnaQUAST(experement, output_dir):
    print("~ running rnaQUASt")
    rnaQUAST = local["rnaQUAST.py"]
    rnaQUAST["-r", experement.ref, "--gtf", experement.gtf, 
            "-c", output_dir + "/transcripts.fasta", "-o", output_dir]()
    print("~ finished rnaQUAST")

def clean_up(output_dir):
    if "madTester" not in output_dir:
        raise RuntimeError("Bad output_dir: " + output_dir)
    print("~ Cleaning up..")
    for item in os.listdir(output_dir):
        if (item != "short_report.txt") and (item != "transcripts_output"):
            if os.path.isdir(os.path.join(output_dir, item)):
                shutil.rmtree(os.path.join(output_dir, item))
            else:
                os.remove(os.path.join(output_dir, item))
    print("~ Done")

def run_experenet(experement, k, corrected_yaml, output_dir):
    if os.path.isdir(output_dir):
        print("Skipping experement " + experement.name 
                + " with k-mer size = " + str(k) + " cause it is already done")
        return
    createdirs(output_dir)
    print("Evaluating experement " + experement.name + " with k-mer size = " + str(k))
    run_rnaSPAdes(experement, k, corrected_yaml, output_dir)
    run_rnaQUAST(experement, output_dir)
    clean_up(output_dir)
    print("Done!") 
    

def main(args):
    check_args(args)
    output_dir = "results" if len(args) < 3 else args[2]
    output_dir += "/madTester" # protection form accidental deletion of unrelated data
    try:
        mad_data = TestData(args[1])
        summary = Summary()
        for exp in mad_data.experements:
            test(exp, output_dir, summary)
        print("Saving results in summary.html")
        f = open(output_dir + "/summary.html", "w")
        f.write(summary.tohtml().tostring())
        f.close()
        print("Done.")
    except DataListExc as datalist_exception:
        print("Invalide DATA_LIST format!")
        print(datalist_exception)

if __name__ == '__main__':
    main(sys.argv)


