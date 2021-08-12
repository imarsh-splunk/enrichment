#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Run this in the app directory

import argparse
import json
import datetime
import os
import re

from collections import OrderedDict

splunk_cr_py_header = """# File: {filename}
# Copyright (c) {year} Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED."""

splunk_cr_html_header = """<!-- File: {filename}
  Copyright (c) {year} Splunk Inc.

  SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
  without a valid written license from Splunk Inc. is PROHIBITED.
-->"""

splunk_cr_header_json = u"Copyright (c) {year} Splunk Inc."


splunk_cr_py_header_re = r"#.*?(?:Copyright).*?(?:Splunk Inc.).*?(?:PROHIBITED.)"
phantom_cr_py_header_re = r"#\s*--.*?(?:Copyright \(c\) Phantom Cyber).*?#\s*--"
# "You shouldn't use regex to match HTLM"
# Yet here we are
splunk_cr_html_header_re = r"<!--[^>]*?(?:Copyright).*?(?:Splunk Inc.).*?(?:PROHIBITED.).*?-->"
phantom_cr_html_header_re = r"<!--[^>]*?(?:Copyright \(c\) Phantom Cyber).*?-->"


cr_year_re = r'([0-9]{4}(?:-[0-9]{4})?)'


def update_year(cr_str, manual_year):
    this_year = str(datetime.datetime.now().year)
    cr_year = re.findall(cr_year_re, cr_str)
    if len(cr_year_re) == 0:
        print "\tNo year found in copyright"
        print "\tUsing this year..."
        cr_year = this_year
    else:
        cr_year = cr_year[0]

    if '-' in cr_year:
        parts = cr_year.split('-')
        cr_year = '-'.join([parts[0], this_year])
    else:
        if cr_year != this_year:
            cr_year = '-'.join([cr_year, this_year])

    if (manual_year is not None):
        if (manual_year == 'current'):
            cr_year = this_year
        else:
            cr_year = manual_year

    return cr_year


def update_cr_file(file_path, new_cr_header, new_cr_re, old_cr_re, manual_year):
    print "Processing file: {}".format(file_path)
    with open(file_path, 'r+') as fp:
        filename = os.path.split(file_path)[-1]
        file_str = fp.read()
        fp.seek(0)

        phantom_cr_regexc = re.compile(old_cr_re, re.MULTILINE | re.DOTALL)
        found = phantom_cr_regexc.findall(file_str)
        if found:
            if len(found) == 1:
                print "\tFound old copyright, updating to new one..."
                year = update_year(found[0], manual_year)
                cr_header = new_cr_header.format(
                    year=year,
                    filename=filename
                )
                file_str = phantom_cr_regexc.sub(cr_header, file_str)
            elif len(found) > 1:
                print "\tMultiple copyright headers found, ignoring file"
                return

        else:
            splunk_cr_regexc = re.compile(new_cr_re, re.MULTILINE | re.DOTALL)
            found = splunk_cr_regexc.findall(file_str)
            if len(found) == 0:
                print "\tNo copyright headers found"
                print "\tAdding copyright header..."
                cr_header = new_cr_header.format(
                    year=datetime.datetime.now().year,
                    filename=filename
                )
                file_str = '{}{}'.format(cr_header, file_str)
            elif len(found) == 1:
                try:
                    cur_cr_year = re.findall(cr_year_re, found[0])[0]
                except:
                    print "\tNo year exists in current copyright header, ignoring file"
                new_cr_year = update_year(found[0], manual_year)
                if new_cr_year != cur_cr_year:
                    print "\tUpdaing copyright header..."
                    cr_header = new_cr_header.format(
                        year=new_cr_year,
                        filename=filename
                    )
                    file_str = splunk_cr_regexc.sub(cr_header, file_str)
            elif len(found) > 1:
                print "\tMultiple copyright headers found, ignoring file"
                return

        fp.write(file_str)
        fp.truncate()
        fp.flush()
        fp.close()
        return


def update_cr_json(file_path, manual_year):
    print "Processing file: {}".format(file_path)
    with open(file_path, 'r+') as fp:
        json_file = json.load(fp, object_pairs_hook=OrderedDict, encoding='utf8')
        if json_file.get('appid') is None:
            print "\tIgnoring file {0}, because it is not an app JSON".format(file_path)
            return
        old_license = json_file['license']
        new_cr_year = update_year(old_license, manual_year)
        new_license = splunk_cr_header_json.format(year=new_cr_year)
        json_file['license'] = new_license
        fp.seek(0)
        s = json.dumps(json_file, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False, encoding='utf8')
        fp.write(s.encode('utf-8'))
        fp.truncate()
        fp.flush()
        fp.close()

    if old_license != new_license:
        print "\tUpdating copyright header"

    return


def main(app_directory, manual_year=None):
    for f in os.listdir(app_directory):
        file_path = os.path.join(app_directory, f)
        if f.endswith('.json'):
            update_cr_json(file_path, manual_year)
        elif f.endswith('.py'):
            update_cr_file(file_path, splunk_cr_py_header, splunk_cr_py_header_re, phantom_cr_py_header_re, manual_year)
        elif f.endswith('.html'):
            update_cr_file(file_path, splunk_cr_html_header, splunk_cr_html_header_re, phantom_cr_html_header_re, manual_year)

    return 0


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Update the copyright of all the files in the App Directory")
    argparser.add_argument('-d', '--app_directory', help="App Directory", default=".")
    argparser.add_argument('-y', '--manual_year', help="Manually set the year, pass the string 'current' to manually set the year to the current year", required=False)

    args = argparser.parse_args()
    d = vars(args)

    exit(main(**d))
