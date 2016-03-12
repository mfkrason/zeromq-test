
def configure(conf):
	conf.load('compiler_cxx')
	conf.env.CXXFLAGS.append('-std=c++11')
	conf.env.PREFIX = './install'

	pass

def options(opt):
	opt.load('compiler_cxx')

	pass

def build(bld):

	sources = bld.path.ant_glob("**/*.cpp")

	bld.program(
			target='runner',
			source=sources,
			)

