import utils_clean


def search_part_with_same_hash_head(text, hash, diff_len):
    stop = len(hash)
    # search start of magic
    start_hash = utils_clean.get_hash(text[:stop], False).strip()
    full_len = len(text) - diff_len
    while start_hash != hash:
        if full_len <= stop:
            return None
        last_stop = stop
        if len(hash) > len(start_hash):
            # try skip difference between hashes
            stop = stop + len(hash) - len(start_hash)
        else:
            if text[stop] not in ("/", "\n", "*"):
                for i in xrange(stop, len(text)):
                    if text[i] in ("/", "\n", "*"):
                        stop = i - 1
                        break
            # looks like not hashable
            stop = stop + 1
        start_hash = utils_clean.get_hash(text[:stop], False).strip()
        if start_hash[:len(hash)] == hash:
            # slowdown search
            stop = last_stop + 1
            start_hash = utils_clean.get_hash(text[:stop], False).strip()
        print "%d%%   \r" % (100 * stop / len(text)),
    return text[:stop]


def search_part_with_same_hash_tail(text, hash, diff_len):
    stop = len(text) - len(hash)
    # search start of magic
    start_hash = utils_clean.get_hash(text[stop:], False)
    while start_hash.strip() != hash:
        if stop <= diff_len:
            return None
        if len(hash) > len(start_hash):
            # try skip difference between hashes
            stop = stop - (len(hash) - len(start_hash))
        else:
            # looks like not hashable
            stop = stop - 1
        start_hash = utils_clean.get_hash(text[stop:], False)
        print "%d%%   \r" % (100 * stop / len(text)),
    return text[stop:]


def optimize_head(src_file, dst_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = utils_clean.cleanup(src_desc.read())
    if not src_text:
        return
    dst_desc = open(dst_file, 'rb')
    with dst_desc:
        dst_text = utils_clean.cleanup(dst_desc.read())
    if not dst_text:
        return
    src_hash = utils_clean.get_hash(src_text, True)
    dst_hash = utils_clean.get_hash(dst_text, True)
    common_hash = None
    for i in xrange(min(len(src_hash), len(dst_hash))):
        if src_hash[i] != dst_hash[i]:
            common_hash = src_hash[:i-1]
            break
    if common_hash:
        common_hash = common_hash.strip()
    while True:
        if common_hash:
            print "diff %s => %s: common head %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
            common_hash_dst = None
            common_hash_src = search_part_with_same_hash_head(
                src_text, common_hash,
                len(src_hash) - len(common_hash)
            )
            if common_hash_src:
                if dst_text[:len(common_hash_src)] == common_hash_src:
                    common_hash_dst = common_hash_src
                else:
                    common_hash_dst = search_part_with_same_hash_head(
                        dst_text, common_hash,
                        len(dst_hash) - len(common_hash)
                    )
            if common_hash_dst and common_hash_src:
                if len(common_hash_dst) < len(common_hash_src):
                    dst_desc = open(dst_file, 'wb')
                    with(dst_desc):
                        dst_desc.write(
                            common_hash_src + dst_text[len(common_hash_dst):]
                        )
                return
            # looks as too long hash
            found_something = False
            for i in xrange(1, len(common_hash)):
                if common_hash[-i] == "\n":
                    common_hash = common_hash[:-i].strip()
                    found_something = True
                    break
            if not found_something:
                print "diff %s => %s: No common head" % (
                    src_file, dst_file
                )
                return
            print "diff %s => %s: try shorter common head %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
        else:
            print "diff %s => %s: no common head" % (src_file, dst_file)
            return


def optimize_tail(src_file, dst_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = utils_clean.cleanup(src_desc.read())
    if not src_text:
        return
    dst_desc = open(dst_file, 'rb')
    with dst_desc:
        dst_text = utils_clean.cleanup(dst_desc.read())
    if not dst_text:
        return
    src_hash = utils_clean.get_hash(src_text, True)
    dst_hash = utils_clean.get_hash(dst_text, True)
    common_hash = None
    for i in xrange(1, min(len(src_hash), len(dst_hash))):
        if src_hash[-i] != dst_hash[-i]:
            if i > 1:
                common_hash = src_hash[-i + 1:]
            break
    while True:
        found_something = False
        if common_hash:
            if common_hash.find("\n") != -1:
                found_something = True
                common_hash = common_hash[common_hash.find("\n"):].strip()
        if common_hash:
            print "diff %s => %s: common tail %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
            common_hash_dst = None
            common_hash_src = search_part_with_same_hash_tail(
                src_text, common_hash,
                len(src_hash) - len(common_hash)
            )
            if common_hash_src:
                if dst_text[:-len(common_hash_src)] == common_hash_src:
                    common_hash_dst = common_hash_src
                else:
                    common_hash_dst = search_part_with_same_hash_tail(
                        dst_text, common_hash,
                        len(dst_hash) - len(common_hash)
                    )
            if common_hash_dst and common_hash_src:
                if len(common_hash_dst) < len(common_hash_src):
                    dst_desc = open(dst_file, 'wb')
                    with(dst_desc):
                        dst_desc.write(
                            dst_text[:-len(common_hash_dst)] + common_hash_src
                        )
                return
            if not found_something:
                print "diff %s => %s: No common tail" % (
                    src_file, dst_file
                )
                return
            # looks as too long hash
            print "diff %s => %s: try shorter common tail %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
        else:
            print "diff %s => %s: no comomn tail " % (src_file, dst_file)
            return


def file_hash(name):
    file_desc = open(name, 'rb')
    with file_desc:
        return utils_clean.get_hash(file_desc.read(), True)
