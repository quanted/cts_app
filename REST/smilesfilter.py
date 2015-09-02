__author__ = 'KWOLFE'


def is_valid_smiles(smiles):

    excludestring = {".",
                         "[Ag]",
                         "[Al]",
                         "[Au]",
                         "[As]",
                         "[As+",
                         "[B]",
                         "[B-]",
                         "[Br-]",
                         "[Ca]",
                         "[Ca+",
                         "[Cl-]",
                         "[Co]",
                         "[Co+",
                         "[Fe]",
                         "[Fe+",
                         "[Hg]",
                         "[K]",
                         "[K+",
                         "[Li]",
                         "[Li+",
                         "[Mg]",
                         "[Mg+",
                         "[Na]",
                         "[Na+",
                         "[Pb]",
                         "[Pb2+]",
                         "[Pb+",
                         "[Pt]",
                         "[Sc]",
                         "[Si]",
                         "[Si+",
                         "[SiH]",
                         "[Sn]",
                         "[W]"
                                }


    if any(x in smiles for x in excludestring):
        return False
    else:
        return True
