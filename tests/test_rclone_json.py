"""
Unit test file.
"""

import unittest

from rclone_api import Config

TEXT = """
{
    "dst": {
        "type": "s3",
        "bucket": "bucket",
        "endpoint": "https://s3.amazonaws.com",
        "access_key_id": "access key",
        "access_secret_key": "access secret key"
    }
}
"""

JSON_DATA = {
    "dst": {
        "type": "s3",
        "bucket": "bucket",
        "endpoint": "https://s3.amazonaws.com",
        "access_key_id": "access key",
        "access_secret_key": "access secret key",
    }
}


def json_to_rclone_config(json_data: dict) -> Config | Exception:
    return Config.from_json(json_data)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_json_to_rclone(self) -> None:
        """Test command line interface (CLI)."""
        rclone_conf = json_to_rclone_config(JSON_DATA)
        self.assertFalse(isinstance(rclone_conf, Exception))
        print(rclone_conf)
        print("done")


if __name__ == "__main__":
    unittest.main()
