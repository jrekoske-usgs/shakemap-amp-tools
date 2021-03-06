#!/usr/bin/env python

# stdlb imports
import os

# third party imports
import numpy as np
from amptools.exception import AmptoolsException
from amptools.io.usc.core import is_usc, read_usc
from amptools.stream import group_channels


def test_usc():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    datadir = os.path.join(homedir, '..', '..', '..', 'data', 'usc')

    files = {
        '017m30cc.y0a': (-.049, .086),
        '017m30lw.e0a': (.046, .004),
        '017m30lw.e0b': (.099, .004),
        '017m30lw.e0c': (-.006, .025),
        '017m30lw.s0a': (-.005, .014),
        '017m30lw.s0b': (.066, -.029),
        '017m30lw.s0c': (-.026, -.018)
    }

    streams = []
    for tfilename, accvals in files.items():
        filename = os.path.join(datadir, tfilename)
        assert is_usc(filename)

        # test acceleration from the file
        stream = read_usc(filename)

        # test for one trace per file
        assert stream.count() == 1

        # test that the traces are acceleration
        for trace in stream:
            assert trace.stats.standard.units == 'acc'
        # compare the start/end points
        np.testing.assert_almost_equal(accvals[0], stream[0].data[0])
        np.testing.assert_almost_equal(accvals[1], stream[0].data[-1])

        # append to list of streams, so we can make sure these group together
        streams.append(stream)

    # test location override
    stream = read_usc(filename, location='test')
    for trace in stream:
        assert trace.stats.location == 'test'

    newstreams = group_channels(streams)
    assert len(newstreams) == 3

    meta_stream = read_usc(os.path.join(datadir, '017m30cc.y0a'))
    stats = meta_stream[0].stats
    assert stats['network'] == 'LA'
    assert stats['station'] == '57'
    assert stats['channel'] == 'HN1'
    assert stats['location'] == '--'
    dt = '%Y-%m-%dT%H:%M:%SZ'
    assert stats['starttime'].strftime(dt) == '1994-01-17T12:30:00Z'
    assert stats['npts'] == 7340
    np.testing.assert_almost_equal(stats.coordinates['latitude'], 34.419, 3)
    np.testing.assert_almost_equal(stats.coordinates['longitude'], -118.426, 3)
    assert str(stats.coordinates['elevation']) == 'nan'
    assert stats.standard['horizontal_orientation'] == 0
    assert stats.standard['instrument_period'] == 0.039
    assert stats.standard['instrument_damping'] == .577
    assert stats.standard['process_time'] == ''
    assert stats.standard['process_level'] == 'V1'
    assert stats.standard['station_name'] == '16628 W. LOST CANYON RD., CANYON COUNTRY, CA'
    assert stats.standard['sensor_serial_number'] == ''
    assert stats.standard['instrument'] == ''
    assert stats.standard['comments'] == ''
    assert stats.standard['units'] == 'acc'
    assert stats.standard['structure_type'] == ''
    assert stats.standard['source_format'] == 'usc'
    assert stats.standard['source'] == 'Los Angeles Basin Seismic Network, University of Southern California'
    assert stats.format_specific['fractional_unit'] == .100

    filename = os.path.join(datadir, '017m30bt.s0a')
    assert is_usc(filename) == True

    # test that volume 2 is not available yet
    try:
        read_usc(filename)
        success = True
    except AmptoolsException:
        success = False
    assert success == False

    # test wrong format exception
    try:
        datadir = os.path.join(homedir, '..', '..', '..', 'data', 'smc')
        read_usc(os.path.join(datadir, '0111b.smc'))
        success = True
    except Exception:
        success = False
    assert success == False




if __name__ == '__main__':
    test_usc()
