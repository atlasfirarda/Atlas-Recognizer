def check(requirement: str = "none") -> bool:
    import subprocess
    import sys
    from importlib.metadata import distribution, PackageNotFoundError

    if requirement == "none":
        try:
            from colorTexts import red, green, yellow
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "colored"])
                from colorTexts import red, green, yellow
            except subprocess.CalledProcessError:
                return False

        requirements: list = []

        with open("settings/requirements.txt", "r") as reqInfo:

            lines = reqInfo.readlines()

            for i in range(0, len(lines)):
                line = lines[i].strip("\n")

                requirements.append(line)

        for req in requirements:
            try:
                distribution(req)
            except PackageNotFoundError:
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req])
                except subprocess.CalledProcessError:
                    return False
        return True
    else:
        try:
            distribution(requirement)
            return True
        except PackageNotFoundError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
                return True
            except subprocess.CalledProcessError:
                return False
