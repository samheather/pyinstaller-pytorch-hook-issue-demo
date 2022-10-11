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
pip uninstall torch torchvision
pip install -U --pre torch torchvision --extra-index-url https://download.pytorch.org/whl/nightly/cpu
```

Initially, I would run pyinstaller using the following:

```
pyinstaller hi.py --noconfirm --clean --target-arch arm64 --hidden-import=pytorch --copy-metadata torch
```

Then I'd add the following after line 22 in the generated `.spec` to give the `hi.spec` included in this repo:
```
tmp_ret = collect_all('torch', include_py_files=True)
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pytorch', include_py_files=True)
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('torchvision', include_py_files=True)
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('timm', include_py_files=True)
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# To handle: https://giters.com/pyinstaller/pyinstaller/issues/6281
tmp_ret = collect_all('basicsr', include_py_files=True)
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
```

I then switch to running pyinstaller using the spec file:

```pyinstaller hi.spec```

## Running the binary you just generated

First, open a new shell window _outside of your venv_

Next, to setup the run-time environment, run the following once, to deal with issues where disttools is imported before setuptools:
```
export SETUPTOOLS_USE_DISTUTILS=stdlib
```

To run the binary, it's required to remove the duplicated dynlibs included at the root of the `dist` folder and link them to those included by pyinstaller. Best do this in a separate shell _outside_ the venv.

```
cd ./dist/hi
rm libtorch_python.dylib
rm libtorch.dylib
rm libc10.dylib
rm libtorch_cpu.dylib
ln -s ./torch/lib/libtorch_python.dylib libtorch_python.dylib
ln -s ./torch/lib/libtorch.dylib libtorch.dylib
ln -s ./torch/lib/libc10.dylib libc10.dylib
ln -s ./torch/lib/libtorch_cpu.dylib libtorch_cpu.dylib
./hi
cd ../../
```

## This is where the problems start

The current error I see is:
```
torchvision/io/image.py:13: UserWarning: Failed to load image Python extension: Failed to load dynlib/dll '/Users/samuel/git/imaginAIry/dist/hi/torchvision/image.so'. Most likely this dynlib/dll was not found when the application was frozen.
  warn(f"Failed to load image Python extension: {e}")
torchvision/__init__.py:23: UserWarning: You are importing torchvision within its own root folder (/Users/samuel/git/imaginAIry/dist/hi). This is not expected to work and may give errors. Please exit the torchvision project source and relaunch your python interpreter.
  warnings.warn(message.format(os.getcwd()))
Traceback (most recent call last):
  File "torch/_sources.py", line 23, in get_source_lines_and_file
    sourcelines, file_lineno = inspect.getsourcelines(obj)
  File "inspect.py", line 1129, in getsourcelines
  File "inspect.py", line 958, in findsource
OSError: could not get source code

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "hi.py", line 2, in <module>
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "imaginairy/__init__.py", line 7, in <module>
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "imaginairy/api.py", line 18, in <module>
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "imaginairy/enhancers/face_restoration_codeformer.py", line 12, in <module>
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "imaginairy/vendored/codeformer/codeformer_arch.py", line 11, in <module>
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "PyInstaller/loader/pyimod02_importers.py", line 499, in exec_module
  File "imaginairy/vendored/codeformer/vqgan_arch.py", line 21, in <module>
  File "torch/jit/_script.py", line 1340, in script
    ast = get_jit_def(obj, obj.__name__)
  File "torch/jit/frontend.py", line 262, in get_jit_def
    parsed_def = parse_def(fn) if not isinstance(fn, _ParsedDef) else fn
  File "torch/_sources.py", line 122, in parse_def
    sourcelines, file_lineno, filename = get_source_lines_and_file(
  File "torch/_sources.py", line 32, in get_source_lines_and_file
    raise OSError(msg) from e
OSError: Can't get source for <function swish at 0x285eb6950>. TorchScript requires source access in order to carry out compilation, make sure original .py files are available.
[738] Failed to execute script 'hi' due to unhandled exception!
```
