import os
import shutil

from checkImports import check

debug = False

dirCategories = os.path.join(os.path.dirname(__file__), "settings", "categories.txt")
dirCustomDir = os.path.join(os.path.dirname(__file__), "settings", "customdir.txt")

if not os.path.exists(dirCategories):
    with open(f"{dirCategories}", "x") as categoryCreate:
        categoryCreate.write("mp4=VIDEO-FILES\npng=IMAGE-FILES")
if not os.path.exists(dirCustomDir):
    with open(f"{dirCustomDir}", "x") as customdirCreate:
        customdirCreate.write("")

try:
    with open("settings/customdir.txt", "r") as customDirRead:
        csDir = customDirRead.readline().strip("\n").replace(" ", "")

        if csDir != "":

            with open("settings/customdir.txt", "w") as customDirWrite:
                csDirWrite = customDirWrite.write(csDir)
        else:
            csDir = ""
except FileNotFoundError:
    csDir = ""


class Main:
    def __init__(self, default: bool = True, customDir: str = "none"):
        self.default = default
        self.customDir = "none" if customDir == "" else customDir
        if self.default and self.customDir == "none":
            self.downloadDir = os.path.join(os.path.expanduser("~"), "Downloads")
        elif self.customDir != "none":
            self.downloadDir = os.path.join(self.customDir)
        elif self.default and self.customDir != "none":
            self.downloadDir = os.path.join(self.customDir)
        elif self.default and self.customDir == "none":
            self.downloadDir = os.path.join(os.path.expanduser("~"), "Downloads")
        else:
            self.downloadDir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.currentDir = os.path.join(os.path.dirname(__file__))
        self.appData = os.path.dirname(os.getenv("appdata"))
        self.tempDir = os.path.join(self.appData, "Local", "Temp")


class App(Main):
    def __init__(self):
        super().__init__()

    @staticmethod
    def getCategories():

        categories: dict = {}
        folders: list = []
        extensions: list = []
        types: list = []

        try:
            with open("settings/categories.txt", "r") as file:
                lines = file.readlines()

                emptyLines = 0

                for x in range(0, len(lines)):
                    findEmpty = lines[x]
                    if findEmpty == "\n":
                        emptyLines += 1

                with open("settings/categories.txt", "w") as fileWrite:
                    for i in range(0, len(lines) - emptyLines):

                        try:
                            line = lines[i].strip("\n").replace(" ", "").split("=")
                            fileWrite.writelines(
                                (line[0] + "=" + line[1] + "\n")
                                if line[0] != "" and line[1] != ""
                                else ""
                            )
                        except IndexError:
                            fileWrite.writelines("")
                            continue

                        if line[0] != "" and line[0] not in extensions:
                            extensions.append(line[0])
                        if line[1] != "":
                            types.append(line[1])
                        if line[1] != "" and line[1] not in folders:
                            folders.append(line[1])
                        if line[0] != "" and line[1] != "":
                            categories.update({line[0]: line[1]})

                    return extensions, types, folders, categories
        except FileNotFoundError:
            return "none"

    def getCategory(self, number: int = 0):

        extension = self.getCategories()[0][number]
        type = self.getCategories()[1][number]

        return extension, type

    def getLength(self):

        length = len(self.getCategories()[0])

        return length

    def createFolders(self, folderDir):

        try:
            for i in self.getCategories()[2]:
                if not os.path.exists(os.path.join(folderDir, f"{i}")):
                    os.makedirs(os.path.join(folderDir, f"{i}"))
            return True
        except Exception:
            return False

    def removeFolders(self, folderDir):
        try:
            for i in self.getCategories()[2]:
                if os.path.exists(os.path.join(folderDir, f"{i}")):
                    shutil.rmtree(os.path.join(folderDir, f"{i}"))
            return True
        except Exception:
            return False

    def move(self, folderDir):

        fileList = os.listdir(folderDir)
        dirList = os.listdir(folderDir)
        folderList = self.getCategories()[2]
        categories = self.getCategories()[3]

        try:
            for j in range(0, len(fileList)):
                for x in fileList:
                    if x in folderList:
                        fileList.remove(x)
            for k in range(0, len(dirList)):
                for l in dirList:
                    if not l in folderList:
                        dirList.remove(l)
            for file in fileList:
                fileExtension = (
                    os.path.splitext(file)[1].__str__().strip(".").lower()[0:]
                )

                for n in categories.keys():
                    if fileExtension == n:
                        extension = n
                        shutil.move(
                            os.path.join(folderDir, f"{file}"),
                            os.path.join(
                                folderDir, f"{categories.get(extension)}", f"{file}"
                            ),
                        )
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":

    importCheck = check()

    if importCheck:

        main = Main(default=True, customDir=rf"{csDir}")
        app = App()

        if debug:
            print(app.createFolders(main.downloadDir))
            print(app.move(main.downloadDir))
        else:
            app.createFolders(main.downloadDir)
            app.move(main.downloadDir)
