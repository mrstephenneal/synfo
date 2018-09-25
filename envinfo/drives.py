from envinfo.system import System

# Windows only, get information on mounted drives
if System().os == 'Windows':
    from os import popen
    from re import findall, MULTILINE
    from string import ascii_uppercase
    from ctypes import windll


    class Drives:
        def __init__(self):
            self.drives = self._get_drives()
            self.drives_local = self._get_drives_local()

        def __str__(self):
            return str(self.drives)

        def __iter__(self):
            return iter(self.drives)

        @staticmethod
        def _get_drives():
            """Get list of all network and locally mounted drives"""
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in ascii_uppercase:
                if bitmask & 1:
                    drives.append(letter)
                bitmask >>= 1

            return ['{0}:\\'.format(d) for d in drives]

        @staticmethod
        def _get_drives_local():
            """Get list of locally mounted drives"""
            return findall(r"[A-Z]+:.*$", popen("mountvol /").read(), MULTILINE)


    def main():
        print(Drives())


    if __name__ == '__main__':
        main()


else:
    print("envinfo.drives module is compatible with Windows platform's only")
