"""TextVerifier Class."""

import sys
import os
import re
import glob
import datetime

import yaml


class TextVerifier:
    _recursive = False
    _config = None
    _pattern = None
    _target_files = []

    def __init__(self, target_path = None):
        self._load_settings()

        if target_path != None:
    	    self._load_targets(target_path)
    
    def _replace_yaml(self, dic, key, src, dest):
        value = dic[key]

        if type(value) is str:
            dic[key] = dic[key].replace(src, dest)
        if type(value) is dict:
            for el_key in value:
                self._replace_yaml(dic[key], el_key, src, dest)
        if type(value) is list:
            replace_list = []
            for el in value:
                replace_list.append(str(el).replace(src, dest))
            dic[key] = replace_list

    def _load_settings(self):
        # config.yaml load
        with open('textverifier/config.yaml') as file :
            self._config = yaml.safe_load(file)
        # pattern.yaml load
        with open('textverifier/pattern.yaml') as file :
            self._pattern = yaml.safe_load(file)

        for key in self._pattern:
            self._replace_yaml(self._pattern, key, '$weekdays$', self._create_weekday_or_text())
        
        # flag to recursive search for directory
        self._recursive = self._config['dir_recursive']

    def _load_targets(self, target_path):
        # search_target_files
        # directory
        if os.path.isdir(target_path):
            for suffix in self._config['target_suffix_list']:
                self._target_files = self._target_files + self._find_all_files(target_path, suffix=suffix)
        # single_file
        else:
            self._target_files.append(target_path)

    def _find_all_files(self, path, suffix="txt"):
        if self._recursive:
            search_path = path + "**/*." + suffix
        else:
            search_path = path + "*." + suffix
        return [os.path.abspath(p) for p in glob.glob(search_path, recursive=self._recursive)]

    def _get_err_print(self, err):
        return "[Err]" + err

    def verify_text(self, text):
        err_list = []

        err_list += self._verify_date_format(text)
        err_list += self._verify_date(text)

        return err_list

    def verify(self):
        """
        Args:
            target_path : file_path or directory_path
        """

        err_count = 0
        for path in self._target_files:
            err_list = []
            with open(path) as f:
                line = f.read()

                err_list += self.verify_text(line)

            # output err
            if len(err_list) > 0 :
                print("[Err file path]" + path, file=sys.stderr)
                for err in err_list:
                    print(err, file=sys.stderr)
                print("", file=sys.stderr)
            err_count = err_count + len(err_list)

    def _verify_date_format(self, text):
        """
        Args:
            text
        Return:
            err_list
        """
        date_pattern_easy = r"%s" % self._pattern['date_format_easy']
        date_pattern = r"%s" % self._pattern['date_format']

        # easy
        matched_list_easy = re.findall(date_pattern_easy, text)

        # tight
        matched_list = re.findall(date_pattern, text)

        diff_list = [e for e in matched_list_easy if e not in matched_list]
        
        err_list = []
        is_err = len(diff_list) > 0
        if is_err:
            for diff in diff_list:
                err_list.append(self._get_err_print("Date format does't conform to rules: " + diff))

        # NG format list check
        if self._pattern['date_format_ng_list'] != None:
            for ng_format in self._pattern['date_format_ng_list']:
                ng_format_pattern = r"%s" % ng_format
                matched_ng_list = re.findall(ng_format_pattern, text)

                for matched_ng in matched_ng_list:
                    matched_ng = matched_ng.replace("\n", "\\n")    # for put the output error on one line
                    err_list.append(self._get_err_print("Date format does't conform to rules(NG list): " + matched_ng))
        
        return err_list

    def _create_weekday_or_text(self):
        result = ""
        weekday_pattern_list = self._pattern['weekday_pattern_list']

        for weekday_pattern in weekday_pattern_list:
            result += weekday_pattern + "|"
        else:
            result = result[0:-1]

        return result

    def _verify_date(self, text):
        """
        Args:
            text
        Return:
            err_list
        """
        
        date_pattern = r"%s" % self._pattern['date_format']
        date_extract_pattern = r"%s" % self._pattern['date_extract_pattern']
        date_extract_patterns = self._pattern['date_extract_patterns']
        weekday_pattern_list = self._pattern['weekday_pattern_list']
        err_list = []
        
        matched_list = re.findall(date_pattern, text)

        for matched_text in matched_list:
            match = re.search(date_extract_pattern, matched_text)

            year = int(match.group(date_extract_patterns['year'])) if date_extract_patterns['year'] > 0 else datetime.date.today().year
            month = int(match.group(date_extract_patterns['month']))
            day = int(match.group(date_extract_patterns['day']))
            weekday = match.group(date_extract_patterns['weekday']) if date_extract_patterns['weekday'] > 0 else None
            
            date = None
            # verify date
            try:
                date = datetime.date(year, month, day)
            except ValueError:
                err_list.append(self._get_err_print("{0}/{1}/{2} isn't exist: {3}".format(year, month, day, matched_text)))
                continue
                
            # verify weekday
            if weekday != None:
                correct_weekday = weekday_pattern_list[int(date.weekday())]
                if correct_weekday != weekday:
                    err_list.append(self._get_err_print("Weekday isn't specified correctly. \"{0}\" is incorrect and \"{1}\" is correct: {2}".format(weekday, correct_weekday, matched_text)))
                    continue
        
        return err_list
