#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
NAS monitor script

Configure directories for RRD files and HTML files in the variables below.
Volumes are in (block device, alias) format. If you plan to add more volumes
or hard disks reserve space for them in the CONF_MAX_* variables.
'''

import sys
import argparse
import synomon.config
import synomon.monitor
from synomon.monitors import *

def cmd_list(args):
    print 'Available monitors and graphs:'
    gm = synomon.graph.all()
            
    for i in sorted(synomon.monitor.all()):
        sys.stdout.write('  %-10.10s: ' % (i))
        if (i in gm):
            print ', '.join(sorted(gm[i]))
        else:
            print '(no graphs defined)'

def cmd_show(args):
    config = synomon.config.Config(args.config_file)
    for i in synomon.monitor.monitors(config):
        i.show()

def cmd_update(args):
    config = synomon.config.Config(args.config_file)
    for i in synomon.monitor.monitors(config):
        i.update()

def cmd_report(args):
    config = synomon.config.Config(args.config_file)

    print 'Generating report...'
    if len(sys.argv) > 2:
        view = sys.argv[2]
    else:
        view = ''

    for i in synomon.graph.graphs(config):
        i.graph(height=150, width=480, view=view)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config-file', metavar='file',
                  action='store', default='/opt/etc/monitor.conf',
                  help='configuration file to use')
    subparser = parser.add_subparsers()
    list_parser = subparser.add_parser('list',
                  help='list all available monitors and graphs')
    list_parser.set_defaults(func=cmd_list)
    show_parser = subparser.add_parser('show',
                  help='show values retrieved by monitors')
    show_parser.set_defaults(func=cmd_show)
    update_parser = subparser.add_parser('update', help='update database')
    update_parser.set_defaults(func=cmd_update)
    report_parser = subparser.add_parser('report', help='generate graphs')
    report_parser.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)




