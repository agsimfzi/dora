import pytest


def test_import_main():
    from dora_pyrealsense.main import main

    # Check that everything is working, and catch dora Runtime Exception as we're not running in a dora dataflow.
    with pytest.raises(ConnectionError):
        main()
