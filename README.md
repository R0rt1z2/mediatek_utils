# MediaTek Utils
Those are some small utils related to MediaTek devices that I created.

## How do they work?
You'll find 3 different utils in this repo (`src/utils/`):
- `cutter.py`: Allows you to cut the header of the Little Kernel (`LK`) or the Preloader (`PL`):
  - `python3 src/utils/cutter.py pl preloader.img`.
  - `python3 src/utils/cutter.py lk lk.img`.
- `dl_handshake.py`: Allows you to handshake a MediaTek device in Preloader (`MT65XX`) or bootROM (`MT6627`) mode:
  - `python3 src/utils/dl_handshake.py -d /dev/ttyACM0` (NOTE: You may want to replace `/dev/ttyACM0` with your correspoding port).
- `preloader_tool.py`: Allows you to analyze the given preloader (supports both preloaders with headers and without):
  - `python3 src/utils/preloader_tool.py --header preloader_with_header.img`.
  - `python3 src/utils/preloader_tool.py preloader_with_no_header.img`.

## License
All the files under this repository are licensed under the **GNU General Public License (v2)**. See LICENSE.MIT and LICENSE.GPL2 for more information.
