from distutils.core import setup

setup(name='bogus',
      version='0.1.5',
      description='A simple bogus server to use in tests',
      author='Globo.com',
      author_email='flavia.missi@corp.globo.com',
      url='https://github.com/globocom/bogus-test-server#bogus-test-server',
      py_modules=["bogus.server"]
     )
