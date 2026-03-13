from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

common_compile_args = ["-std=c++17"]
common_link_args = ["-lmongocxx", "-lbsoncxx", "-lpthread"]
common_include_dirs = [
    "/opt/homebrew/include",
    "/opt/homebrew/include/mongocxx/v_noabi",
    "/opt/homebrew/include/bsoncxx/v_noabi",
    "./parallel_hashmap"
]

common_library_dirs = ["/opt/homebrew/lib"]

cython_dirs = "cython"
shared_cpp_sources = ["cpp/MongoManager.cpp", "cpp/Trie.cpp", "cpp/TrieNode.cpp"]

ext_modules = [
    Extension(
        name="Route",
        sources=[f"{cython_dirs}/Route.pyx"],
        extra_compile_args=common_compile_args,
        language="c++",
    ),
    Extension(
        name="RouteTable",
        sources=[f"{cython_dirs}/RouteTable.pyx"] + shared_cpp_sources,
        include_dirs=common_include_dirs,
        library_dirs=common_library_dirs,
        extra_compile_args=common_compile_args,
        extra_link_args=common_link_args,
        language="c++",
    ),
    Extension(
        name="Extension",
        sources=[f"{cython_dirs}/Extension.pyx"],
        extra_compile_args=common_compile_args,
        language="c++",
    ),
    Extension(
        name="Message",
        sources=[f"{cython_dirs}/Message.pyx"],
        extra_compile_args=common_compile_args,
        language="c++",
    ),
    Extension(
        name="AS",
        sources=[f"{cython_dirs}/AS.pyx"] + shared_cpp_sources,
        include_dirs=common_include_dirs,
        library_dirs=common_library_dirs,
        extra_compile_args=common_compile_args,
        extra_link_args=common_link_args,
        language="c++",
    ),
    Extension(
        name="Topology",
        sources=[f"{cython_dirs}/Topology.pyx"] + shared_cpp_sources,
        include_dirs=common_include_dirs,
        library_dirs=common_library_dirs,
        extra_compile_args=common_compile_args,
        extra_link_args=common_link_args,
        language="c++",
    ),
    Extension(
        name="Processor",
        sources=[f"{cython_dirs}/Processor.pyx"] + shared_cpp_sources,
        include_dirs=common_include_dirs,
        library_dirs=common_library_dirs,
        extra_compile_args=common_compile_args,
        extra_link_args=common_link_args,
        language="c++",
    ),
    Extension(
        name="Scheduler",
        sources=[f"{cython_dirs}/Scheduler.pyx"] + shared_cpp_sources,
        include_dirs=common_include_dirs,
        library_dirs=common_library_dirs,
        extra_compile_args=common_compile_args,
        extra_link_args=common_link_args,
        language="c++",
    ),
]

setup(
    ext_modules=cythonize(
        ext_modules,
    ),
    cmdclass={"build_ext": build_ext},
)
