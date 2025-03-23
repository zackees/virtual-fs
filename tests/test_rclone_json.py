"""
Unit test file.
"""

import json
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


def _json_to_rclone_config(json_data: dict) -> str:
    """Convert JSON data to rclone config."""
    out = ""
    for key, value in json_data.items():
        out += f"[{key}]\n"
        for k, v in value.items():
            out += f"{k} = {v}\n"
    return out


def json_to_rclone_config(json_data: dict) -> Config | Exception:
    try:
        text = _json_to_rclone_config(json_data)
        return Config(text=text)
    except Exception as e:
        return e


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_json_conversion(self) -> None:
        """Test command line interface (CLI)."""
        data = json.dumps(JSON_DATA, indent=4)
        print(data)
        data = json.loads(TEXT)
        print(data)
        self.assertEqual(JSON_DATA, data)
        print("done")

    def test_json_to_rclone(self) -> None:
        """Test command line interface (CLI)."""
        rclone_conf = _json_to_rclone_config(JSON_DATA)
        print(rclone_conf)
        print("done")


if __name__ == "__main__":
    unittest.main()
