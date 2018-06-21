import os
from distutils.core import run_setup
from shutil import copyfile, rmtree

SOURCE_FILENAME = 'example.py'
BUILD_PATH = 'dist'


def get_source(filename):
    with open(filename, 'r') as fp:
        return fp.read()


class ExtractHiddenBlock(object):
    start_block_delimiter = "# START HIDDEN BLOCK"
    end_block_delimiter = "# END HIDDEN BLOCK"

    source_lines = []

    block_lines = []

    def get_source(self):
        return "\n".join(self.source_lines)

    def get_block_source(self):
        return "\n".join(self.block_lines)

    def preprocess(self, source):

        lines = source.split("\n")

        in_block = False
        removed_block = False

        for line in lines:
            if self.start_block_delimiter in line:
                if in_block:
                    raise RuntimeError(
                        "Encountered nested begin hidden tests statements"
                    )

                in_block = True
                removed_block = True

            elif self.end_block_delimiter in line:
                in_block = False

            elif not in_block:
                self.source_lines.append(line)

            elif in_block:
                self.block_lines.append(line)

        if in_block:
            raise RuntimeError("No end hidden tests statement found")

        if removed_block:
            self.block_lines.append("\n")

        return removed_block


def main():
    source = get_source(SOURCE_FILENAME)
    extract = ExtractHiddenBlock()

    removed_block = extract.preprocess(source)

    if removed_block:
        new_source = "from tests import *\n" + extract.get_source()
    else:
        new_source = source

    # build
    os.makedirs(BUILD_PATH, exist_ok=True)

    # write new source file
    with open(os.path.join(BUILD_PATH, SOURCE_FILENAME), 'w') as fp:
        fp.write(new_source)

    if removed_block:
        # write new tests package
        test_package_path = os.path.join(BUILD_PATH, 'tests')
        os.makedirs(test_package_path, exist_ok=True)

        with open(os.path.join(test_package_path, '__init__.py'), 'w') as fp:
            fp.write('from .funcs import *')

        block_source = extract.get_block_source()
        with open(os.path.join(test_package_path, 'funcs.py'), 'w') as fp:
            fp.write(block_source)

        # compile
        setup_file = os.path.join(test_package_path, 'setup.py')
        copyfile('setup.tmpl.py', setup_file)

        # compile & cleanup
        os.chdir(test_package_path)
        run_setup('setup.py', ['build_ext', '--inplace'])

        rmtree('build')
        os.remove('setup.py')
        os.remove('funcs.c')
        os.remove('funcs.py')

    print('done.')


if __name__ == '__main__':
    main()
