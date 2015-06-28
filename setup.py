from distutils.core import setup

setup(name='albhed.py',
      version='0.1',
      description='An AlBhed Translator written in Python',
      author='Lord Yuuma von Combobreaker',
      author_email='lordyuuma@gmail.com',
      license="WTFPL",

      packages=['albhed'],
      py_modules=['albhed.maps', 'albhed.translators', 'albhed.utils'],
      package_dir={'': 'src'},

      scripts=['scripts/albhed', 'scripts/spiran']
      )
