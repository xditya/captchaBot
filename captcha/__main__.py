# (c) 2022 @xditya.
# Powered by apis.xditya.me

import importlib
import logging
import glob
from pathlib import Path
import sys
from . import log, bot, whoami

log.info("Loading plugins...")
path = "captcha/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        plugin_name = plugin_name.replace(".py", "")
        path = Path(f"captcha/plugins/{plugin_name}.py")
        name = "captcha.plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(name, path)
        load = importlib.util.module_from_spec(spec)
        load.logger = logging.getLogger(plugin_name)
        spec.loader.exec_module(load)
        sys.modules["captcha.plugins." + plugin_name] = load
log.info("Loaded all plugins.")

if __name__ == "__main__":
    bot.loop.run_until_complete(whoami())
    bot.run_until_disconnected()
