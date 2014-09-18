import sys
import pyusf


def print_and_exit(s):
    print >> sys.stderr, s
    sys.exit(1)

def add_sample(rdist_hist, rdist):
    if rdist_hist.has_key(rdist):
        rdist_hist[rdist] += 1
    else:
        rdist_hist[rdist] = 1

def filter_true(begin, end, rdist):
    return True

def usf_read_events(usf_file, line_size, filter=filter_true):
    rdist_burst_hist = []

    assert(not (usf_file.header.flags & pyusf.USF_FLAG_TRACE))
    burst_mode = usf_file.header.flags & pyusf.USF_FLAG_BURST
    if not burst_mode:
        rdist_burst_hist.append(({}, {}))

    for event in usf_file:
        if isinstance(event, pyusf.Burst):
            if burst_mode:
                rdist_burst_hist.append(({}, {}))
            else:
                print >> sys.stderr, "Warning: Ignored burst event in " \
                    "non-burst file."
            continue

        assert(isinstance(event, pyusf.Sample) or \
                   isinstance(event, pyusf.Stride) or \
                   isinstance(event, pyusf.Dangling) or \
                   isinstance(event, pyusf.Stride) or \
                   isinstance(event, pyusf.Smptrace) )

        if not isinstance(event, pyusf.Smptrace):
            if (1 << event.line_size) != line_size:
                continue

        (rdist_hist, frdist_hist) = rdist_burst_hist[-1]
        if isinstance(event, pyusf.Sample):
            assert(event.begin.time < event.end.time)
            rdist = event.end.time - event.begin.time - 1
        elif isinstance(event, pyusf.Dangling):
            rdist = sys.maxint
        else:
            continue

        add_sample(rdist_hist, rdist)
        if filter(event.begin,
                  event.end if isinstance(event, pyusf.Sample) else None,
                  rdist):
            add_sample(frdist_hist, rdist)

    return rdist_burst_hist

def parse_usf(file_name, line_size, filter=filter_true):
    try:
        usf_file = pyusf.Usf()
        usf_file.open(file_name)
    except IOError, e:
        print_and_exit(str(e))

    if usf_file.header.flags & pyusf.USF_FLAG_TRACE:
        print_and_exit("XXX")

    if not usf_file.header.line_sizes & line_size:
        print_and_exit("Line size (%i) not available in USF file." % line_size)

    rdist_burst_hist = usf_read_events(usf_file,
                                       line_size=line_size,
                                       filter=filter)

    usf_file.close()
    return rdist_burst_hist
