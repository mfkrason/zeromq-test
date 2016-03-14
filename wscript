
from waflib.Build import BuildContext

import os

def configure(conf):
	conf.load('compiler_cxx')
	conf.env.CXXFLAGS.append('-std=c++11')
        conf.options.prefix = './install'

        conf.check_cxx(lib='zmqpp', uselib_store='ZMQPP', linkflags='-L/home/mfkrason/.linuxbrew/lib')
        conf.check_cxx(lib='zmq', uselib_store='ZMQ', linkflags='-L/home/mfkrason/.linuxbrew/lib')

	pass

def options(opt):
	opt.load('compiler_cxx')
	pass

def collect( self, target, srcs ):
    dct = getattr( self, target, [] )

    dct += [ os.path.join( repr(self.path), x ) for x in srcs]

    print dct

    setattr( self, target, dct )

def build(bld):

    BuildContext.collect = collect

    bld.recurse('src')

    """
    bld(
        features='cxx cxxshlib',
        target='client_lib',
        srcs=bld.client_lib,
        )
    """

    bld(
        features='cxx cxxshlib',
        target='server_lib',
        #source=bld.server_lib,
        source='src/server/Server.cpp',
        includes=['src', '/home/mfkrason/.linuxbrew/include'],
        libpath='/home/mfkrason/.linuxbrew/lib',
        use=['ZMQPP', 'zmq'],
        )

    bld(
        features='cxx cxxprogram',
        target='server',
        source='src/server/main.cpp',
        includes=['src'],
        libpath='/home/mfkrason/.linuxbrew/lib',
        use='ZMQPP ZMQ server_lib'.split(),
        )


