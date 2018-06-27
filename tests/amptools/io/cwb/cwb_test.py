#!/usr/bin/env python

# stdlib imports
import os
import tempfile

# third party imports
import numpy as np

# local imports
from amptools.io.cwb.core import is_cwb, read_cwb, _get_header_info


def test():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    datadir = os.path.join(homedir, '..', '..', '..', 'data', 'cwb')
    cwb_file = os.path.join(datadir, '1-EAS.dat')
    assert is_cwb(cwb_file)
    try:
        assert is_cwb(os.path.abspath(__file__))
    except AssertionError:
        assert 1 == 1
    stream = read_cwb(cwb_file)
    np.testing.assert_almost_equal(
        np.abs(stream[0].max()), 0.83699999999999997)
    assert stream[0].stats['sampling_rate'] == 50

    cwb_file = os.path.join(datadir, '2-ECU.dat')
    assert is_cwb(cwb_file)
    try:
        assert is_cwb(os.path.abspath(__file__))
    except AssertionError:
        assert 1 == 1
    stream = read_cwb(cwb_file)
    for trace in stream:
        stats = trace.stats
        assert stats['station'] == 'ECU'
        assert stats['sampling_rate'] == 50
        dt = '%Y-%m-%dT%H:%M:%SZ'
        assert stats['starttime'].strftime(dt) == '2018-02-06T15:50:29Z'
        assert stats.standard['station_name'] == 'Chulu'
        assert stats.standard['instrument'] == 'FBA'
        assert stats.coordinates['latitude'] == 22.860
        assert stats.coordinates['longitude'] == 121.092
        assert stats.format_specific['dc_offset_hhz'] == -1.017
        assert stats.format_specific['dc_offset_hhn'] == -2.931
        assert stats.format_specific['dc_offset_hhe'] == -2.811
        defaulted = ['instrument_period', 'instrument_damping',
                     'process_time', 'corner_frequency']
        for default in defaulted:
            assert str(stats.standard[default]) == 'nan'
        defaulted = ['comments', 'structure_type', 'sensor_serial_number']
        for default in defaulted:
            assert stats.standard[default] == ''
    # Test alternate defaults
    missing_info = """#Earthquake Information
    \n#Origin Time(GMT+08): 2018/02/06-23:50:42
    \n#EpicenterLongitude(E): 121.69
    \n#EpicenterLatitude(N): 24.14
    \n#Depth(km): 10.0
    \n#Magnitude(Ml): 6.0
    \n#Station Information
    \n#StationCode: ECU
    \n#StartTime(GMT+08): 2018/02/06-23:50:29.000
    \n#RecordLength(sec): 120
    \n#SampleRate(Hz): 50
    \n#AmplitudeUnit:  gal. DCoffset(corr)
    \n#DataSequence: Time U(+); N(+); E(+)
    \n#Data: 4F10.3
         0.000     0.000     0.000     0.000
         0.020     0.000     0.000     0.000
         0.040     0.000     0.000     0.000
         0.060     0.000     0.000     0.000
         0.080     0.000     0.000     0.000
         0.100     0.000     0.000     0.000
         0.120     0.000     0.000     0.000
            """
    tmp = tempfile.NamedTemporaryFile(delete=True)
    with open(tmp.name, 'w') as f:
        f.write(missing_info)
    f = open(tmp.name, 'rt')
    data = stream[0].data
    data = np.reshape(data, (int(len(data)/2), 2), order='C')
    metadata = _get_header_info(open(tmp.name, 'rt'), data)
    tmp.close()
    assert str(metadata['coordinates']['longitude']) == 'nan'
    assert str(metadata['coordinates']['latitude']) == 'nan'
    assert metadata['standard']['station_name'] == ''
    assert metadata['standard']['instrument'] == ''
    assert str(metadata['format_specific']['dc_offset_hhz']) == 'nan'
    assert str(metadata['format_specific']['dc_offset_hhe']) == 'nan'
    assert str(metadata['format_specific']['dc_offset_hhn']) == 'nan'


if __name__ == '__main__':
    test()
