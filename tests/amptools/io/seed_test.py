#!/usr/bin/env python


from amptools.io.seedname import get_channel_name


def test_channel():
    rate = 50
    tchannel1 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=False, is_north=True)
    assert tchannel1 == 'BN1'

    tchannel2 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=False, is_north=False)
    assert tchannel2 == 'BN2'

    tchannel3 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=True, is_north=False)
    assert tchannel3 == 'BNZ'

    rate = 100
    tchannel4 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=False, is_north=True)
    assert tchannel4 == 'HN1'

    tchannel5 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=False, is_north=False)
    assert tchannel5 == 'HN2'

    tchannel6 = get_channel_name(rate, is_acceleration=True,
                                 is_vertical=True, is_north=False)
    assert tchannel6 == 'HNZ'

    tchannel4 = get_channel_name(rate, is_acceleration=False,
                                 is_vertical=False, is_north=True)
    assert tchannel4 == 'HH1'


if __name__ == '__main__':
    test_channel()
