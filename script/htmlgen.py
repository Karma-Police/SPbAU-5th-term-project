class HTMLPage:
    def __init__(self):
        self.code = []

    def addp(self, s):
        self.code.append("<p>" + s + "</p>")

    def addh1(self, s):
        self.code.append("<h1>" + s + "</h1>")

    def addh2(self, s):
        self.code.append("<h2>" + s + "</h2>")

    def addtable(self, table, header):
        res = "<table cellspacing=3>"
        if header is not None:
            res += HTMLPage.tablerow(header)
        for r in table:
            res += HTMLPage.tablerow(r)
        res += "</table>"
        self.code.append(res)

    @staticmethod
    def tablerow(row):
        res = ""
        if row is not None:
            res += "<tr>"
            for r in row:
                res += "<td>" + r + "</td>"
            res += "</tr>"
        return res

    def tostring(self):
        return ''.join(self.code)
