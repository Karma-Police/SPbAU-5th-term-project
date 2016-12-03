import sys
sys.path.append("/home/mnikonov/.local/lib/python3.5/site-packages")

from datalist import *
from plumbum import local

def show_usage():
    print("MadTester v0.1")
    print("Usage: MadTester DATA_LIST [OUTPUT_DIR]")

def check_args(args):
    if not 1 < len(args) < 4:
        show_usage()
        exit()

def main(args):
    check_args(args)
    mad_data = TestData(args[1], "results" if len(args) < 3 else args[2])
    for e in mad_data.experements:
        print(e.name)
        print(e.ref)
#    run_SPAdes(mad_data)
#    run_rnaQUAST(mad_data)

if __name__ == '__main__':
    main(sys.argv)
