class Biomarker():

    # constructor
    def __init__(self, name, units, mean, std, min, max):
        self.name = name,
        self.units = units, # eg. "ng/mg_creatinine"
        self.mean = 10.0,
        self.std = 3.0,
        self.min = 0.0,
        self.max = 30.0

    # TODO : lookup_literature function for vals

    def __init__(self, schema): # schema is a JSON file
        pass
