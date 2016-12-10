import sys
import re
from htmlgen import *

class Summary:
    def __init__(self):
        self.reports = {}

    def addrep(self, test_name, kval, repfile):
        if test_name not in self.reports:
            self.reports[test_name] = []
        self.reports[test_name].append(Report(kval, repfile))

    def tohtml(self):
        page = HTMLPage()        
        page.addh1("SPAdes and rnaQUAST test results")
        for name, reps in self.reports.items():
            page.addh2("For " + name);
            page.addtable(Report.totable(reps), None)
        return page
            

class Report:
    def __init__(self, kval, repfile):
        self.kval = str(kval)
        lines = ["zero line"] + repfile.readlines()
        assert(len(lines) == 46)
        self.dbmetrics = DatabaseMetrics(Report.valfrom(lines[6]), Report.valfrom(lines[7]))
        self.basic_transcripts_metrics = BasicTranscriptsMetrics(
                Report.valfrom(lines[10]), Report.valfrom(lines[11]), Report.valfrom(lines[12]))
        self.alignment_metrics = AlignmentMetrics(Report.valfrom(lines[15]), 
                Report.valfrom(lines[16]), Report.valfrom(lines[17]), Report.valfrom(lines[18]))
        self.metrics_for_nonmisassembled_tr = AlignmentMetricsForNONmisTranscripts(
            Report.valfrom(lines[21]), Report.valfrom(lines[22]), Report.valfrom(lines[23]))
        self.metrics_for_misassembled_tr = AMetricsForMisassembledTranscripts(
                Report.valfrom(lines[26]))
        self.assembly_completeness = AssemblyCompleteness(Report.valfrom(lines[29]), 
            Report.valfrom(lines[30]), Report.valfrom(lines[31]), Report.valfrom(lines[32]), 
            Report.valfrom(lines[33]), Report.valfrom(lines[34]), Report.valfrom(lines[35]), 
            Report.valfrom(lines[36]), Report.valfrom(lines[37]), Report.valfrom(lines[38]), 
            Report.valfrom(lines[39]))
        self.assembly_specifity = AssemblySpecifity(Report.valfrom(lines[42]), 
                Report.valfrom(lines[43]), Report.valfrom(lines[44]), Report.valfrom(lines[45]))

    @staticmethod
    def valfrom(s):
        res = re.search(r'(\d|\.)+\W*$', s)
        return res.group() if res else "Not found!"

    @staticmethod
    def totable(reps):
        kvals = ["K-mer size"]
        dbmetrics = []
        basic_tr = []
        alignment_metrics = []
        metrics_for_nonmis = []
        metrics_for_mis = []
        assembly_compl = []
        assembly_specifity = []
        for r in reps:
            kvals.append(r.kval)
            dbmetrics.append(r.dbmetrics)
            basic_tr.append(r.basic_transcripts_metrics)
            alignment_metrics.append(r.alignment_metrics)
            metrics_for_nonmis.append(r.metrics_for_nonmisassembled_tr)
            metrics_for_mis.append(r.metrics_for_misassembled_tr)
            assembly_compl.append(r.assembly_completeness)
            assembly_specifity.append(r.assembly_specifity)
        return [kvals] \
                + DatabaseMetrics.tolist(dbmetrics) \
                + BasicTranscriptsMetrics.tolist(basic_tr) \
                + AlignmentMetrics.tolist(alignment_metrics) \
                + AlignmentMetricsForNONmisTranscripts.tolist(metrics_for_nonmis) \
                + AMetricsForMisassembledTranscripts.tolist(metrics_for_mis) \
                + AssemblyCompleteness.tolist(assembly_compl) \
                + AssemblySpecifity.tolist(assembly_specifity)


class DatabaseMetrics:
    def __init__(self, genes, anoepi):
        self.genes = genes
        self.anoepi = anoepi
    @staticmethod
    def tolist(metrics_list):
        genes = ["Genes"]
        anoepi = ["Avg. number of exons per isoform"]
        for dbm in metrics_list:
            genes.append(dbm.genes)
            anoepi.append(dbm.anoepi)
        return [genes, anoepi]


class BasicTranscriptsMetrics:
    def __init__(self, transcripts, transcripts500, transcripts1000):
        self.transcripts = transcripts
        self.transcripts500 = transcripts500
        self.transcripts1000 = transcripts1000
    @staticmethod
    def tolist(basictm):
        transcripts = ["Transcripts"]
        transcripts500 = ["Transcripts > 500 bp"]
        transcripts1000 = ["Transcripts > 1000 bp"]
        for btm in basictm:
            transcripts.append(btm.transcripts)
            transcripts500.append(btm.transcripts500)
            transcripts1000.append(btm.transcripts1000)
        return [transcripts, transcripts500, transcripts1000]


class AlignmentMetrics:
    def __init__(self, aligned, uniqaligned, multaligned, unaligned):
        self.aligned = aligned
        self.uniqaligned = uniqaligned
        self.multaligned = multaligned
        self.unaligned = unaligned
    @staticmethod
    def tolist(alignment_metrics):
        aligned = ["Aligned"]
        uniqaligned = ["Uniquely aligned"]
        multaligned = ["Multiply aligned"]
        unaligned = ["Unaligned"]
        for entry in alignment_metrics:
            aligned.append(entry.aligned)
            uniqaligned.append(entry.uniqaligned)
            multaligned.append(entry.multaligned)
            unaligned.append(entry.unaligned)
        return [aligned, uniqaligned, multaligned, unaligned]


class AlignmentMetricsForNONmisTranscripts:
    def __init__(self, avg_aligned_fr, avg_aligned_len, avg_mism):
        self.avg_aligned_fr = avg_aligned_fr
        self.avg_aligned_len = avg_aligned_len
        self.avg_mism = avg_mism
    @staticmethod
    def tolist(amfnmt):
        avg_aligned_fr = ["Avg. aligned fraction"]
        avg_aligned_len = ["Avg. alignment length"]
        avg_mism = ["Avg. mismatches per transcript"]
        for entry in amfnmt:
            avg_aligned_fr.append(entry.avg_aligned_fr)
            avg_aligned_len.append(entry.avg_aligned_len)
            avg_mism.append(entry.avg_mism)
        return [avg_aligned_fr, avg_aligned_len, avg_mism]


class AMetricsForMisassembledTranscripts:
    def __init__(self, misassemblies):
        self.misassemblies = misassemblies
    @staticmethod
    def tolist(amfmt):
        misassemblies = ["Misassemblies"]
        for entry in amfmt:
            misassemblies.append(entry.misassemblies)
        return [misassemblies]


class AssemblyCompleteness:
    def __init__(self, dc, ag50, ag95, cg50, cg95, ai50, ai95, ci50, ci95, mic, mia):
        self.dc = dc
        self.ag50 = ag50
        self.ag95 = ag95
        self.cg50 = cg50
        self.cg95 = cg95
        self.ai50 = ai50
        self.ai95 = ai95
        self.ci50 = ci50
        self.ci95 = ci95
        self.mic = mic
        self.mia = mia
    @staticmethod
    def tolist(completeness):
        dc = ["Database coverage"]
        ag50 = ["50%-assembled genes"]
        ag95 = ["95%-assembled genes"]
        cg50 = ["50%-covered genes"]
        cg95 = ["95%-covered genes"]
        ai50 = ["50%-assembled isoforms"]
        ai95 = ["95%-assembled isoforms"]
        ci50 = ["50%-covered isoforms"]
        ci95 = ["95%-covered isoforms"]
        mic = ["Mean isoform coverage"]
        mia = ["Mean isoform assembly"]
        for entry in completeness:
            dc.append(entry.dc)
            ag50.append(entry.ag50)
            ag95.append(entry.ag95)
            cg50.append(entry.cg50)
            cg95.append(entry.cg95)
            ai50.append(entry.ai50)
            ai95.append(entry.ai95)
            ci50.append(entry.ci50)
            ci95.append(entry.ci95)
            mic.append(entry.mic)
            mia.append(entry.mia)
        return [dc, ag50, ag95, cg50, cg95, ai50, ai95, ci50, ci95, mic, mia]


class AssemblySpecifity:
    def __init__(self, matched50, matched95, unannotated, mfota):
        self.matched50 = matched50
        self.matched95 = matched95
        self.unannotated = unannotated
        self.mfota = mfota
    @staticmethod
    def tolist(assembly_specifity):
        matched50 = ["50%-matched"]
        matched95 = ["95%-matched"]
        unannotated = ["Unannotated"]
        mfota = ["Mean fraction of transcript matched"]
        for entry in assembly_specifity:
            matched50.append(entry.matched50)
            matched95.append(entry.matched95)
            unannotated.append(entry.unannotated)
            mfota.append(entry.mfota)
        return [matched50, matched95, unannotated, mfota]


