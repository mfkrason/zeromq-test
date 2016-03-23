
from waflib.Build import BuildContext, Options

import os,sys
import pprint

def configure(conf):
    conf.load('compiler_cxx')

    conf.env.CXXFLAGS.append('-std=c++11')
    conf.env.append_value('LINKFLAGS', '-L/home/mfkrason/.linuxbrew/lib')
    conf.env.append_value('RPATH', conf.env['PREFIX'] + '/lib' )
    conf.env.append_value('RPATH', '/home/mfkrason/.linuxbrew/lib')
    conf.env.append_value('CXXFLAGS', '-I'+os.path.abspath('./src'))
    conf.env.append_value('CXXFLAGS', '-I/home/mfkrason/.linuxbrew/include')
    conf.env.append_value('CXXFLAGS', '-std=c++14')
    conf.env.append_value('CXXFLAGS', '-ggdb')

    conf.check_cxx(lib='zmqpp', uselib_store='ZMQPP', linkflags='-L/home/mfkrason/.linuxbrew/lib')
    conf.check_cxx(lib='zmq', uselib_store='ZMQ', linkflags='-L/home/mfkrason/.linuxbrew/lib')

def options(opt):
    opt.load('compiler_cxx')
    #opt.get_option_group('configure options'). set_defaults(prefix=os.path.abspath('./install')
    opt.parser.set_defaults(prefix=os.path.abspath('./install'))

def collect( self, target, srcs ):
    print target, srcs
    dct = getattr( self, target, [] )

    dct += [ os.path.relpath( repr(self.path), x ) for x in srcs]

    setattr( self, target, dct )

def build(bld):

    BuildContext.collect = collect

    bld.recurse('src')
    print 80*'*'
    print bld.client_lib

    bld(
        features='cxx cxxshlib',
        target='client_lib',
        #source=' '.join(bld.client_lib),
        source = './src/client/Client.cpp',
        )

    bld(
        features='cxx cxxshlib',
        target='server_lib',
        #source=bld.server_lib,
        source='src/server/Server.cpp',
        use=['ZMQPP', 'zmq'],
        )

    bld(
        features='cxx cxxprogram',
        target='server',
        source='src/server/main.cpp',
        use='ZMQPP ZMQ server_lib'.split(),
        )

    bld(
        features='cxx cxxprogram',
        target='client',
        source='src/client/main.cpp',
        use='ZMQPP ZMQ client_lib'.split(),
        )

