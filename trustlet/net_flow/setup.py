from distutils.core import setup, Extension

extension_mod = Extension("_net_flowmodule",
                          ["lib/_net_flowmodule.cc", "lib/net_flow.cc"],
                          libraries=['glib-2.0', 'stdc++'],
                          include_dirs=['/usr/include/glib-2.0',
                                        '/usr/lib/glib-2.0/include'])

setup(name="net_flow",
      package_dir = {'': 'lib'},
      py_modules = ['net_flow', 'advogato'],
      ext_modules=[extension_mod,])
