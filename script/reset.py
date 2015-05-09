import os
import sys
import utils_clean
import utils_fuzzy_logic


def process_copy(src_file, dst_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = src_desc.read()
    if not src_text:
        return
    dst_desc = open(dst_file, 'rb')
    with dst_desc:
        dst_text = utils_clean.cleanup(dst_desc.read())
    if not dst_text:
        return
    src_text = utils_clean.cleanup(src_text)
    dst_text = utils_clean.cleanup(dst_text)
    if dst_text != src_text:
        dst_desc = open(dst_file, 'wb')
        with(dst_desc):
            dst_desc.write(src_text)
        print "update done: %s => %s" % (src_file, dst_file)
    else:
        print "update unnecessary: %s => %s" % (src_file, dst_file)


def process_file(src_file, dst_file):
    if os.access(src_file, os.R_OK) and os.access(dst_file, os.R_OK):
        need_copy = False
        if src_file.endswith('.c') or \
           src_file.endswith('.h'):
            src_file_hash = utils_fuzzy_logic.file_hash(src_file)
            dst_file_hash = utils_fuzzy_logic.file_hash(dst_file)
            if dst_file_hash == src_file_hash:
                need_copy = True
        elif src_file.endswith('Kconfig') or \
                src_file.endswith('.s') or \
                src_file.endswith('.S'):
            src_file_hash = utils_clean.cleanup(src_file)
            dst_file_hash = utils_clean.cleanup(dst_file)
            if dst_file_hash == src_file_hash:
                need_copy = True

        if need_copy:
            process_copy(src_file, dst_file)
        else:
            print "skiped: %s => %s" % (src_file, dst_file)


def process(src_inode, dst_inode):
    if os.path.isfile(dst_inode) and os.path.isfile(src_inode):
        process_file(src_inode, dst_inode)
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
                    dst_file = src_file.replace(src_inode, dst_inode)
                    process_file(src_file, dst_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print """"
            usage: python reset.py linux-3.4 android_kernel_htc_z4u"
            script for copy same code from one dir to other without
            relation to comments
        """
    else:
        process(sys.argv[1], sys.argv[2])
