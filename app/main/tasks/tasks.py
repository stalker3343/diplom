from .BlueGate.BlueGate import CVE_2020_0609
from .SOCMAP.SOCMAP import CVE_2022_21907
from .SMBGhost.SMBGhost import CVE_2021_44142
from .SambaVuln.SambaVuln import CVE_2020_0796
from .Vonahisec.Vonahisec import CVE_2022_41040
from .CodeSetRelating.CodeSetRelating import CVE_2022_47966


tasks = {
    "BlueGate": lambda target, gradation: CVE_2020_0609(target, gradation),
    "SOCMAP": lambda target, gradation: CVE_2022_21907(target, gradation),
    "SMBGhost": lambda target, gradation: CVE_2021_44142(target, gradation),
    "SambaVuln": lambda target, gradation: CVE_2020_0796(target, gradation), #done
    "Vonahisec": lambda target, gradation: CVE_2022_41040(target, gradation),
    "CodeSetRelating": lambda target, gradation: CVE_2022_47966(target, gradation)
}
