"""
All information about a test is given in a special data_list file. The module parses
data_list and wraps it's records.

"""

from itertools import zip_longest


class TestData: 
    def __init__(self, data_list_file):
        self.experements = []
        self.parse_data_list(data_list_file)
    
    def parse_data_list(self, list_file):
        with open(list_file, 'r') as f:
            lines = f.read().splitlines()
            if len(lines) % 5 != 0:
                raise DataListExc("Bad lines number in DATA_LIST")
            for name, ref, gtf, r1, r2 in zip_longest(*([iter(lines)]*5)):
                TestData.check_note_structure(name, ref, gtf, r1, r2)
                self.experements.append(TestData.experement_from(name, ref, gtf, r1, r2))

    @staticmethod
    def experement_from(name, ref, gtf, r1, r2):
        return Experement(name[len("# "):], ref[len("ref: "):], 
                            gtf[len("grf: "):], r1[len("r1: "):], r2[len("r2: "):])

    @staticmethod
    def check_note_structure(name, ref, gtf, r1, r2):
        if not name.startswith("# "):
            raise DataListExc("Expected test name: [# test_name]")
        if not ref.startswith("ref: "):
            raise DataListExc("Expected reference path: [ref: ref_path]")
        if not gtf.startswith("gtf: "):
            raise DataListExc("Expected gtf path: [gtf: gtf_path]")
        if not r1.startswith("r1: "):
            raise DataListExc("Expected left reads in format [r1: file1&file2&file3]")
        if not r2.startswith("r2: "):
            raise DataListExc("Expected right reads in format [r2: file1&file2&file3]")

class Experement:
    def __init__(self, name, ref, gtf, r1, r2):
        self.name = name
        self.ref = ref
        self.gtf = gtf
        self.r1 = r1.split('&')
        self.r2 = r2.split('&')
        if len(self.r1) != len(self.r2):
            raise DataListExc("Not the same number of left and right reads")

class DataListExc(Exception):
    pass
