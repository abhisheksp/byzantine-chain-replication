import shutil
import tempfile
import unittest
from os import path

import util
import testutil


class TestUtilTest(unittest.TestCase):
    def test_state_equality(self):
        test_dir = tempfile.mkdtemp()
        temp_file_path = path.join(test_dir, 'test_config.txt')
        with open(temp_file_path, 'w') as f:
            f.write('failures[0,0] = client_request(2,1), crash(); shuttle(1,3),sleep(5)\n' +
                    'failures[1,2] = result_shuttle(0,1),drop(); shuttle(1,3),drop()\n' +
                    'failures[1,1] = wedge_request(2), truncate_history(3)'
                    )

        config = util.read_configuration(temp_file_path)
        actual = testutil.parse_failure_scenarios(config)
        expected = {}
        expected[1, 1] = {(3, 2, 'client_request', 'crash'): None, (2, 4, 'shuttle', 'sleep'): 5}
        expected[2, 3] = {(1, 2, 'result_shuttle', 'drop'): None, (2, 4, 'shuttle', 'drop'): None}
        expected[2, 2] = {(3, 'wedge_request', 'truncate_history'): 3}
        shutil.rmtree(test_dir)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
