class Table:
    def __init__(self, args):
        self.colNameList =[]
        self.colNumber = len(args)
        self.indexes = []
        self.data = []
        indexed = 0
        i=0
        for arg in args:
            if arg[1] == "0":
                indexed = 0
            elif arg[1] == "1":
                indexed = 1
                self.indexes.append(i)

            self.colNameList.append([arg[0].strip(), indexed])
            i += 1

    def insertT(self, args):
        if len(args) != self.colNumber:
            print("Number of inserted columns doesn`t coincide with numbers in table")
            return
        self.data.append(args)

    def selectT1(self,cols,where):
        print_data = []
        headers = []
        colname = ""
        colname1 = ""
        value = ""
        oper =""
        if len(where) > 1:
            oper = where[2][0]
            if where[0][1] == "value":
                value = where[0][0]
                colname = where[1][0]
            elif where[1][1] == "value":
                value = where[1][0]
                colname = where[0][0]
            else:
                colname = where[0][0]
                colname1 = where[1][0]
        delind = []
        if colname1 == "":
            k = 0
            ind = -1
            for name in self.colNameList:
                if name[0] == colname:
                    ind = k
                    break
                k += 1
            if ind != -1:
                for c in range(0, len(self.data)):
                    if oper =="=":
                        if self.data[c][ind][0] != value:
                            delind.append(c)
                    elif oper ==">":
                        if self.data[c][ind][0] <= value:
                            delind.append(c)
                    elif oper =="<":
                        if self.data[c][ind][0] >= value:
                            delind.append(c)
                    elif oper ==">=":
                        if self.data[c][ind][0] < value:
                            delind.append(c)
                    elif oper =="<=":
                        if self.data[c][ind][0] > value:
                            delind.append(c)
                    elif oper =="!=":
                        if self.data[c][ind][0] == value:
                            delind.append(c)
            elif len(where) > 1:
                print("Unknown column name in where statement!")
                return
        else:
            ind1 = -1
            ind2 = -1
            k1 = 0
            for name in self.colNameList:
                if name[0] == colname:
                    ind1 = k1
                    break
                k1 += 1
            k2 = 0
            for name in self.colNameList:
                if name[0] == colname1:
                    ind2 = k2
                    break
                k2 += 1
            if ind1 != -1 and ind2 != -1:
                for c in range(1, len(self.data)):
                    if oper =="=":
                        if self.data[c][ind1][0] != self.data[c][ind1][0]:
                            delind.append(c)
                    elif oper ==">":
                        if self.data[c][ind1][0] <= self.data[c][ind1][0]:
                            delind.append(c)
                    elif oper =="<":
                        if self.data[c][ind1][0] >= self.data[c][ind1][0]:
                            delind.append(c)
                    elif oper ==">=":
                        if self.data[c][ind1][0] < self.data[c][ind1][0]:
                            delind.append(c)
                    elif oper =="<=":
                        if self.data[c][ind1][0] > self.data[c][ind1][0]:
                            delind.append(c)
                    elif oper =="!=":
                        if self.data[c][ind1][0] == self.data[c][ind1][0]:
                            delind.append(c)
            else:
                print("Unknown column name in where statement!")
                return
        ind = []
        if len(cols)<=1:
            i = 0
            for el in self.colNameList:
                headers.append(el[0])
                ind.append(i)
                i += 1
            print_data.append(headers)
        else:
            i = 0

            for el in self.colNameList:
                if el[0] in cols:
                    headers.append(el[0])
                    ind.append(i)
                i += 1
            if len(cols) > len(ind):
                print("Unknown column name was selected!")
                return
            print_data.append(headers)
        row = []
        y =0
        for rw in self.data:
            c = 0
            if y not in delind:
                for el in rw:
                    if c in ind:
                        row.append(el[0])
                    c += 1
                row1 = row.copy()
                print_data.append(row1)
                row.clear()
            y+=1

        self.print_pretty_table(print_data)


    def selectT2(self,tbl2,cols,join,where):
        if len(join)<=1:
            headers = []
            for el in self.colNameList:
                headers.append(el)
            for el in tbl2.colNameList:
                headers.append(el)
            tblnew = Table(headers)
            for row1 in self.data:
                for row2 in tbl2.data:
                    tblnew.insertT(row1+row2)
            tblnew.selectT1(cols,where)
        else:
            cln1 = join[0]
            cln2 = join[1]
            ind1 =-1
            i =0
            headers = []
            for el in self.colNameList:
                headers.append(el)
                if el[0]==cln1 and el[1]==1:
                    ind1=i
                i+=1
            i=0
            ind2=-1
            for el in tbl2.colNameList:
                headers.append(el)
                if el[0]==cln2 and el[1]==1:
                    ind2=i
                i+=1
            tblnew = Table(headers)
            if ind2 == -1 or ind1 == -1:
                print("Columns in join statement aren`t indexed or there are no columns with same names!")
                return

            for i in range(0,len(self.data)):
                for j in range(0,len(tbl2.data)):
                    if self.data[i][ind1][0]==tbl2.data[j][ind2][0]:
                        tblnew.insertT(self.data[i] + tbl2.data[j])


            tblnew.selectT1(cols, where)

    def print_pretty_table(self, data, cell_sep=' | ', header_separator=True):
        rows = len(data)
        cols = len(data[0])

        col_width = []
        for col in range(cols):
            columns = [data[row][col] for row in range(rows)]
            col_width.append(len(max(columns, key=len)))

        separator = "-+-".join('-' * n for n in col_width)

        for i, row in enumerate(range(rows)):
            if i == 1 and header_separator:
                print(separator)

            result = []
            for col in range(cols):
                item = data[row][col].rjust(col_width[col])
                result.append(item)

            print(cell_sep.join(result))

    def deleteT(self,where):
        if len(where)>1:
            colname = ""
            colname1 = ""
            value = ""
            if len(where) > 1:
                oper = where[2][0]
                if where[0][1] == "value":
                    value = where[0][0]
                    colname = where[1][0]
                elif where[1][1] == "value":
                    value = where[1][0]
                    colname = where[0][0]
                else:
                    colname = where[0][0]
                    colname1 = where[1][0]
            delind = []
            if colname1 == "":
                k = 0
                ind = -1
                for name in self.colNameList:
                    if name[0] == colname:
                        ind = k
                        break
                    k += 1
                if ind != -1:
                    for c in range(0, len(self.data)):
                        if self.data[c][ind][0] == value:
                            delind.append(c)
                else:
                    print("Unknown column name in where statement!")
                    return
            else:
                ind1 = -1
                ind2 = -1
                k1 = 0
                for name in self.colNameList:
                    if name[0] == colname:
                        ind1 = k1
                        break
                    k1 += 1
                k2 = 0
                for name in self.colNameList:
                    if name[0] == colname1:
                        ind2 = k2
                        break
                    k2 += 1
                if ind1 != -1 and ind2 != -1:
                    for c in range(1, len(self.data)):
                        if self.data[c][ind1][0] == self.data[c][ind2][0]:
                            delind.append(c)
                else:
                    print("Unknown column name in where statement!")
                    return
            for i in range(0, len(delind)):
                del self.data[delind[len(delind) - 1 - i]]
            print(len(delind),end="" )

            print(" rows were deleted from table ",end="")
        else:
            self.data.clear()
