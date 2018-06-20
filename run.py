import ast
import astor
import os
from shutil import copyfile, rmtree
from distutils.core import run_setup

SOURCE_FILENAME = 'example.py'
BUILD_PATH = 'dist'


def get_tree(filename):
    with open(filename, 'r') as fp:
        return ast.parse(fp.read())


class TestFuncTransformer(ast.NodeTransformer):
    prefix = 'test_'

    func_nodes = []

    def visit_FunctionDef(self, node):
        if node.name.startswith(self.prefix):
            # print(node.name)
            self.func_nodes.append(node)
            return None

        return node


def main():
    tree = get_tree(SOURCE_FILENAME)

    transform = TestFuncTransformer()
    tree = transform.visit(tree)

    import_node = ast.ImportFrom('tests', [ast.alias(name='*', asname=None)], 0)
    tree.body.insert(0, import_node)

    # build
    os.makedirs(BUILD_PATH, exist_ok=True)

    # write new source file
    with open(os.path.join(BUILD_PATH, SOURCE_FILENAME), 'w') as fp:
        fp.write(astor.to_source(tree))

    # write new tests package
    test_package_path = os.path.join(BUILD_PATH, 'tests')
    os.makedirs(test_package_path, exist_ok=True)
    with open(os.path.join(test_package_path, '__init__.py'), 'w') as fp:
        fp.write('from .funcs import *')

    funcs = ast.Module(body=transform.func_nodes)
    with open(os.path.join(test_package_path, 'funcs.pyx'), 'w') as fp:
        fp.write(astor.to_source(funcs))

    # compile
    setup_file = os.path.join(test_package_path, 'setup.py')
    copyfile('setup.py.orig', setup_file)

    os.chdir(test_package_path)
    run_setup('setup.py', ['build_ext', '--inplace'])

    # cleanup
    rmtree('build')
    os.remove('setup.py')
    os.remove('funcs.c')
    os.remove('funcs.pyx')

    print('done.')


if __name__ == '__main__':
    main()
