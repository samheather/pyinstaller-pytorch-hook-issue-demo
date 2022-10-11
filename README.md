# Environment tested on:
 * MacOS 12.5.1, M1 Pro MacBook Pro, 32GB RAM
 * Python 3.10.7
 * Rust - installed **directly** (not via Homebrew) - i.e. via `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` as per https://www.rust-lang.org/tools/install

# Steps to reproduce:

**Note:** Rust must be installed prior to executing the below

```
git clone https://github.com/samheather/pyinstaller-pytorch-hook-issue-demo
cd pyinstaller-pytorch-hook-issue-demo
python3 -m venv venv
source venv/bin/activate
pip install -r req.txt

#Finally, try running pyinstaller:
pyinstaller demo.py --noconfirm --clean --target-arch arm64 --hidden-import=pytorch --copy-metadata torch
```

At the final step, the following will be output and the binary produced will fail to execute:
```
38678 DEBUG: Signing file '/Users/samuel/Library/Application Support/pyinstaller/bincache00_py310_64bit/arm64/adhoc/no-entitlements/torch/_C.cpython-310-darwin.so'
Traceback (most recent call last):
  File "/Users/samuel/git/imaginAIry/venv/bin/pyinstaller", line 8, in <module>
    sys.exit(run())
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/__main__.py", line 179, in run
    run_build(pyi_config, spec_file, **vars(args))
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/__main__.py", line 60, in run_build
    PyInstaller.building.build_main.main(pyi_config, spec_file, **kwargs)
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/build_main.py", line 962, in main
    build(specfile, distpath, workpath, clean_build)
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/build_main.py", line 884, in build
    exec(code, spec_namespace)
  File "/Users/samuel/git/imaginAIry/demo.spec", line 53, in <module>
    coll = COLLECT(
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/api.py", line 876, in __init__
    self.__postinit__()
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/datastruct.py", line 173, in __postinit__
    self.assemble()
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/api.py", line 908, in assemble
    fnm = checkCache(
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/building/utils.py", line 381, in checkCache
    osxutils.binary_to_target_arch(cachedfile, target_arch, display_name=fnm)
  File "/Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/PyInstaller/utils/osx.py", line 323, in binary_to_target_arch
    raise IncompatibleBinaryArchError(
PyInstaller.utils.osx.IncompatibleBinaryArchError: /Users/samuel/git/imaginAIry/venv/lib/python3.10/site-packages/torch/_dl.cpython-310-darwin.so is incompatible with target arch arm64 (has arch: x86_64)!
```
