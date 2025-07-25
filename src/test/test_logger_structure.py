import json

from core.logging.logger import get_logger


def validate_log_structure():
    logger = get_logger("test-logger")
    test_message = "Validation test message"

    import io

    stream = io.StringIO()
    handler = logger.handlers[0]
    handler.stream = stream

    logger.info(test_message)
    stream.seek(0)

    # Capture first log line
    output_line = stream.readline().strip()
    try:
        log_dict = json.loads(output_line)
    except json.JSONDecodeError:
        raise AssertionError("❌ Log output is not valid JSON")

    assert log_dict["message"] == test_message
    assert log_dict["levelname"] == "INFO"
    assert "asctime" in log_dict
    assert "filename" in log_dict
    assert "lineno" in log_dict
    assert log_dict["name"] == "test-logger"

    print("✅ Log structure is valid and includes all required fields.")


if __name__ == "__main__":
    validate_log_structure()
