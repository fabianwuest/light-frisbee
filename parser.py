import argparse


def get_main_parser():
    # top-level parser
    parser = argparse.ArgumentParser(
        epilog='',
        prog=''
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='Light Frisbee 1.0.0',
        help='show light frisbee version'
    )

    sps = parser.add_subparsers(dest='cmd')

    # subparser for the start command
    sps_start = sps.add_parser('start',
                               help='',
                               formatter_class=argparse.RawTextHelpFormatter
                               )

    # positional arguments
    sps_start.add_argument('password',
                           action='store',
                           type=str,
                           help='set otree admin password',
                           metavar='admin-password'
                           )

    sps_start.add_argument('link',
                           action='store',
                           type=str,
                           help='set link to the experiment frisbee server',
                           metavar='link'
                           )

    sps_start.add_argument('label',
                           action='store',
                           type=str,
                           help='set participant label',
                           metavar='label'
                           )

    # options
    sps_start.add_argument('-t', '--test-mode',
                           action='store_true',
                           help='set test mode\nif set, thingspeak integration is omitted'
                           )

    # TODO: review this
    sps_start.add_argument('--sample-wait',  # sample-rate / sample-time
                           action='store',
                           type=float,
                           default=0,
                           help='set length of time to wait between retrieving the state of the underlying device'
                           )

    sps_start.add_argument('--send-rate',  # TODO: dependency on sample-wait?
                           action='store',
                           type=float,
                           default=1,
                           help='send'
                           )

    sps_start.add_argument('--gpio-pin',
                           action='store',
                           type=int,
                           default=11,
                           help='set gpio pin that the device is connected to'
                           )

    sps_start.add_argument('--mode',
                           action='store',
                           type=str,
                           default='change',
                           choices=['value', 'change'],
                           help='set mode of operation'
                                '\nvalue: send read value'
                                '\nchange: send read value only if it has changed'
                           )

    sps_start.add_argument('--no-output',
                           action='store_true',
                           help='none of the read values or detected changes are displayed in the console'
                           )

    return parser
