import sys

configFile = open("/home/auxilium/.config/youtube-viewer/api.json", "r+")
configLines = configFile.readlines()

import sys
if sys.argv[1] == "api":
    if len(sys.argv) != 2:
        with open("/home/auxilium/.config/youtube-viewer/api.json", "w") as file:
            file.writelines(["{\n", "    \"key\":           \""+ sys.argv[2] + "\",\n", configLines[2] , configLines[3], configLines[4] ])
elif sys.argv[1] == "cred":
    if len(sys.argv) != 3:
        with open("/home/auxilium/.config/youtube-viewer/api.json", "w") as file:
            file.writelines(["{\n", configLines[1], "   \"client_id\":     \"" + sys.argv[2] + "\",\n", "    \"client_secret\": \"" + sys.argv[3] + "\"\n", configLines[4] ])

