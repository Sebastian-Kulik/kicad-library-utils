# -*- coding: utf-8 -*-

from rules.rule import *

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad lib files.
    """
    def __init__(self, component):
        super(Rule, self).__init__(component, 'For components with a single default footprint, footprint field is filled with valid footprint filename')

    def check(self):
        """
        Proceeds the checking of the rule.
        """

        fail = False

        # Footprint field is index [2]
        if len(self.component.fields) >= 3:
            fp = self.component.fields[2]
            fp_name = fp['name']

            # Strip the quote characters
            if fp_name.startswith('"') and fp_name.endswith('"'):
                fp_name = fp_name[1:-1]

            fp_desc = "Footprint field '{fp}' ".format(fp=fp_name)

            # Only check if there is text in the name
            if len(fp_name) > 0:
                #footprint field should be set to invisible (if it has any text in it)
                if fp['visibility'] == 'V':
                    fail = True
                    self.error(fp_desc + "must be set to invisible.")

                # Footprint field should be of the format "Footprint_Library:Footprint_Name"
                if fp_name.count(":") is not 1 or fp_name.startswith(":") or fp_name.endswith(":"):
                    fail = True
                    self.error(fp_desc + "must be of the format '<Library>:<Footprint>'")

                # Footprint name cannot contain any illegal pathname characters
                else:
                    fp_split = fp_name.split(":")

                    fp_dir = fp_split[0]
                    fp_path = fp_split[1]

                    if not isValidName(fp_dir):
                        self.error("Footprint library '{f}' contains illegal characters".format(f=fp_dir))
                        fail = True

                    if not isValidName(fp_path):
                        self.error("Footprint name '{f}' contains illegal characters".format(f=fp_path))
                        fail = True

                    # Check that the footprint exists!
                    if not fail:
                        if self.footprints_dir and os.path.exists(self.footprints_dir) and os.path.isdir(self.footprints_dir):

                            fp_libs = [x.replace('.pretty', '') for x in os.listdir(self.footprints_dir) if x.endswith('.pretty')]

                            if not fp_dir in fp_libs:
                                self.error('Specified footprint library does not exist')
                                self.errorExtra("Footprint library '{l}' was not found".format(l=fp_dir))
                            else:
                                fp_dir = os.path.join(self.footprints_dir, fp_dir + ".pretty")
                                fp_file = os.path.join(fp_dir, fp_path + '.kicad_mod')

                                if not os.path.exists(fp_file):
                                    self.warning("Specified footprint does not exist")
                                    self.warningExtra("Footprint file {l}:{f} was not found".format(l=fp_dir, f=fp_path))


        return fail

    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        self.info("FIX: not supported")
