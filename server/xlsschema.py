import xlrd


class SchemaXls:
    def __init__(self, file_):
        workbook = xlrd.open_workbook(file_contents=file_, encoding_override="cp1252")
        worksheet = workbook.sheet_by_index(0)  # ottengo il primo foglio
        self.sheet = worksheet
        self.ncol = self.sheet.ncols
        self.nrow = self.sheet.nrows

        self.schema = {}
        for i in xrange(self.ncol):
            v = self.sheet.cell(0,i).value
            self.schema[v] = i

    def get_rows_where(self,**kwargs):
        res = []
        for i in xrange(1,self.nrow):
            row = self.sheet.row(i)
            ok = True
            for k,v in kwargs.items():
                n = self.schema[k]
                if row[n].value != v:
                    ok = False
                    break
            if ok == True:
                res.append(row)
        return res

    def get_first_row_where(self, **kwargs):
        return self.get_rows_where(**kwargs)[0]

    def get_campo(self, row, campo):
        n = self.schema[campo]
        return row[n].value

    def get_campo_where(self, campo, **kwargs):
        row = self.get_first_row_where(**kwargs)
        return self.get_campo(row, campo)

    def get_rows_list(self):
        res = []
        for i in xrange(1,self.nrow):
            r = self.sheet.row(i)
            res.append(r)
        return res

    def get_rows_list_schema(self):
        rows = self.get_rows_list()
        res = []
        for r in rows:
            item = self.get_row_schema(r)
            res.append(item)
        return res

    def get_row_schema(self, row):
        item = {}
        for k, v in self.schema.items():
            item[k.upper()] = row[v].value
        return item
