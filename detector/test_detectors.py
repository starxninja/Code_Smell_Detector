"""
Test file for code smell detectors
"""

import unittest
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detectors import (
    LongMethodDetector, GodClassDetector, DuplicatedCodeDetector,
    LargeParameterListDetector, MagicNumbersDetector, FeatureEnvyDetector
)
from utils import load_config


class TestDetectors(unittest.TestCase):
    """Test cases for code smell detectors"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = load_config('config.yaml')
        self.test_code = '''
class TestClass:
    def __init__(self):
        self.field1 = 1
        self.field2 = 2
        self.field3 = 3
        self.field4 = 4
        self.field5 = 5
        self.field6 = 6
        self.field7 = 7
        self.field8 = 8
        self.field9 = 9
        self.field10 = 10
        self.field11 = 11
        self.field12 = 12
        self.field13 = 13
        self.field14 = 14
        self.field15 = 15
        self.field16 = 16
    
    def long_method(self):
        """This is a very long method with many lines"""
        x = 1
        y = 2
        z = 3
        a = 4
        b = 5
        c = 6
        d = 7
        e = 8
        f = 9
        g = 10
        h = 11
        i = 12
        j = 13
        k = 14
        l = 15
        m = 16
        n = 17
        o = 18
        p = 19
        q = 20
        r = 21
        s = 22
        t = 23
        u = 24
        v = 25
        w = 26
        x = 27
        y = 28
        z = 29
        a = 30
        b = 31
        c = 32
        d = 33
        e = 34
        f = 35
        g = 36
        h = 37
        i = 38
        j = 39
        k = 40
        l = 41
        m = 42
        n = 43
        o = 44
        p = 45
        q = 46
        r = 47
        s = 48
        t = 49
        u = 50
        v = 51
        w = 52
        x = 53
        y = 54
        z = 55
        a = 56
        b = 57
        c = 58
        d = 59
        e = 60
        f = 61
        g = 62
        h = 63
        i = 64
        j = 65
        k = 66
        l = 67
        m = 68
        n = 69
        o = 70
        p = 71
        q = 72
        r = 73
        s = 74
        t = 75
        u = 76
        v = 77
        w = 78
        x = 79
        y = 80
        z = 81
        a = 82
        b = 83
        c = 84
        d = 85
        e = 86
        f = 87
        g = 88
        h = 89
        i = 90
        j = 91
        k = 92
        l = 93
        m = 94
        n = 95
        o = 96
        p = 97
        q = 98
        r = 99
        s = 100
        return x + y + z
    
    def method_with_many_params(self, param1, param2, param3, param4, param5, param6, param7, param8):
        """Method with too many parameters"""
        return param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8
    
    def method_with_magic_numbers(self):
        """Method with magic numbers"""
        if self.field1 > 85:
            return 1000
        elif self.field1 > 70:
            return 500
        elif self.field1 > 50:
            return 200
        else:
            return 0
    
    def similar_method(self):
        """Method similar to another one"""
        if self.field1 > 85:
            return 1000
        elif self.field1 > 70:
            return 500
        elif self.field1 > 50:
            return 200
        else:
            return 0
    
    def another_similar_method(self):
        """Another method similar to the previous ones"""
        if self.field1 > 85:
            return 1000
        elif self.field1 > 70:
            return 500
        elif self.field1 > 50:
            return 200
        else:
            return 0


class AnotherClass:
    def __init__(self):
        self.data = "some data"
    
    def method_that_uses_other_class_data(self, test_instance):
        """Method that uses more data from other class than its own"""
        # More operations on other class data
        result1 = test_instance.field1 + test_instance.field2
        result2 = test_instance.field3 * test_instance.field4
        result3 = test_instance.field5 - test_instance.field6
        
        # Only one operation on own data
        own_result = self.data.upper()
        
        return result1 + result2 + result3 + len(own_result)
'''
    
    def test_long_method_detector(self):
        """Test long method detection"""
        detector = LongMethodDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect the long_method
        self.assertGreater(len(smells), 0)
        long_method_smells = [s for s in smells if s['smell_type'] == 'LongMethod']
        self.assertGreater(len(long_method_smells), 0)
    
    def test_god_class_detector(self):
        """Test god class detection"""
        detector = GodClassDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect the TestClass as god class
        self.assertGreater(len(smells), 0)
        god_class_smells = [s for s in smells if s['smell_type'] == 'GodClass']
        self.assertGreater(len(god_class_smells), 0)
    
    def test_large_parameter_list_detector(self):
        """Test large parameter list detection"""
        detector = LargeParameterListDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect method_with_many_params
        self.assertGreater(len(smells), 0)
        param_smells = [s for s in smells if s['smell_type'] == 'LargeParameterList']
        self.assertGreater(len(param_smells), 0)
    
    def test_magic_numbers_detector(self):
        """Test magic numbers detection"""
        detector = MagicNumbersDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect magic numbers
        self.assertGreater(len(smells), 0)
        magic_smells = [s for s in smells if s['smell_type'] == 'MagicNumbers']
        self.assertGreater(len(magic_smells), 0)
    
    def test_duplicated_code_detector(self):
        """Test duplicated code detection"""
        detector = DuplicatedCodeDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect duplicated code
        self.assertGreater(len(smells), 0)
        dup_smells = [s for s in smells if s['smell_type'] == 'DuplicatedCode']
        self.assertGreater(len(dup_smells), 0)
    
    def test_feature_envy_detector(self):
        """Test feature envy detection"""
        detector = FeatureEnvyDetector(self.config)
        smells = detector.detect('test.py', self.test_code)
        
        # Should detect feature envy
        self.assertGreater(len(smells), 0)
        envy_smells = [s for s in smells if s['smell_type'] == 'FeatureEnvy']
        self.assertGreater(len(envy_smells), 0)


if __name__ == '__main__':
    unittest.main()
