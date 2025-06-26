# import asyncio
# import platform

# import uvicorn
# from shiva import app

# if platform.system() != 'Windows':
#     import uvloop


# # UVLOOP
# loop = asyncio.get_event_loop()
# asyncio.set_event_loop(loop)

# if platform.system() != 'Windows':
#     uvloop.install()

import re
import sys

from shiva.shiva_cli import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
