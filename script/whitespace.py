import os
import sys
import utils_clean


def process_file(src_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = src_desc.read()
    if not src_text:
        return
    dst_text = utils_clean.cleanup(src_text)
    if len(dst_text) < len(src_text):
        dst_desc = open(src_file, 'wb')
        with(dst_desc):
            dst_desc.write(dst_text)
        print "update: " + src_file
    else:
        print "update unnecessary: " + src_file


def process(src_inode):
    if os.path.isfile(src_inode):
        process_file(src_inode)
    else:
        for dirname, _, filenames in os.walk(src_inode):
            # print path to all filenames.
            for filename in filenames:
                if filename.endswith('.c') or \
                   filename.endswith('.h') or \
                   filename.endswith('.s') or \
                   filename.endswith('.S') or \
                   filename.endswith('Kconfig') or \
                   filename == 'Kconfig':
                    src_file = os.path.join(dirname, filename)
                    process_file(src_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print """
            usage: python whitespace.py android_kernel_htc_z4u
            little optimize whitespaces
        """
    else:
        process(sys.argv[1])
