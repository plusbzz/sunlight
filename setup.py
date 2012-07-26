from distutils.core import setup
import sys

sys.path.append('fec')
import fec


setup(name='fec',
      version='0.1',
      author='Raj Bandyopadhyay',
      package_dir={'': 'fec'},
      py_modules=['fec'],
      provides=['fec'],
     )