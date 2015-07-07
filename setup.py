######################################################################
# This program is free software. It comes without any warranty, to   #
# the extent permitted by applicable law. You can redistribute it    #
# and/or modify it under the terms of the Do What The Fuck You Want  #
# To Public License, Version 2, as published by Sam Hocevar. See     #
# http://www.wtfpl.net/ for more details.                            #
######################################################################

from distutils.core import setup

setup(name='albhed.py',
      version='0.1',
      description='An AlBhed Translator written in Python',
      author='Lord Yuuma von Combobreaker',
      author_email='lordyuuma@gmail.com',
      license="WTFPL",

      packages=['albhed'],
      package_dir={'': 'src'},

      scripts=['scripts/albhed', 'scripts/spiran']
      )
