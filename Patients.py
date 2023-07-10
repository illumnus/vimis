class Patients_base:
    def __init__(self):
        self.Number = []
        self.Code = []
        self.mom_FIO = []
        self.child_FIO = []
        self.uniqueNumber = []
        self.date = []
        self.birth_date = []
        self.take_time = []

    def add_volume(self,
                   Number,
                   Code,
                   mom_FIO,
                   child_FIO,
                   uniqueNumber,
                   date,
                   birth_date,
                   take_time):
        try:
            Number = int(''.join(filter(str.isdigit, Number)))
            self.Number.append(Number)
        except:
            self.Number.append(None)

        try:
            Code = int(''.join(filter(str.isdigit, Code)))
            self.Code.append(Code)
        except:
            self.Code.append(None)

        try:
            self.mom_FIO.append(mom_FIO)
        except:
            self.mom_FIO.append(None)

        try:
            self.child_FIO.append(child_FIO)
        except:
            self.child_FIO.append(None)

        try:
            uniqueNumber = int(''.join(filter(str.isdigit, uniqueNumber)))
            self.uniqueNumber.append(uniqueNumber)
        except:
            self.uniqueNumber.append(None)

        try:
            self.date.append(date)
        except:
            self.date.append(None)

        try:
            self.birth_date.append(birth_date)
        except:
            self.birth_date.append(None)

        try:
            self.take_time.append(take_time)
        except:
            self.take_time.append(None)