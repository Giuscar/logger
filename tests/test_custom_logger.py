import unittest
import json
import logging
import re
from io import StringIO
from custom_logger import CustomLogger, CustomFormatter, get_logger


class TestCustomFormatter(unittest.TestCase):
    """Test cases for CustomFormatter class."""

    def test_formatter_init_text_format(self):
        """Test CustomFormatter initialization with text format."""
        formatter = CustomFormatter(format='text')
        self.assertEqual(formatter.output_format, 'text')

    def test_formatter_init_json_format(self):
        """Test CustomFormatter initialization with json format."""
        formatter = CustomFormatter(format='json')
        self.assertEqual(formatter.output_format, 'json')

    def test_formatter_invalid_format(self):
        """Test CustomFormatter raises error with invalid format."""
        with self.assertRaises(ValueError):
            CustomFormatter(format='invalid')

    def test_formatter_default_format(self):
        """Test CustomFormatter defaults to text format."""
        formatter = CustomFormatter()
        self.assertEqual(formatter.output_format, 'text')

    def test_formatter_custom_datefmt(self):
        """Test CustomFormatter with custom date format."""
        custom_datefmt = '%d/%m/%Y %H:%M:%S'
        formatter = CustomFormatter(datefmt=custom_datefmt)
        self.assertEqual(formatter.datefmt, custom_datefmt)


class TestCustomLogger(unittest.TestCase):
    """Test cases for CustomLogger class."""

    def setUp(self):
        """Set up test fixtures."""
        # Remove any existing handlers to avoid interference
        for logger_name in list(logging.Logger.manager.loggerDict):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

    def test_logger_init_default(self):
        """Test CustomLogger initialization with defaults."""
        logger = CustomLogger(name='test_logger')
        self.assertEqual(logger.name, 'test_logger')
        self.assertEqual(logger._logger.level, logging.INFO)

    def test_logger_init_custom_level(self):
        """Test CustomLogger initialization with custom level."""
        logger = CustomLogger(name='test_logger', level=logging.DEBUG)
        self.assertEqual(logger._logger.level, logging.DEBUG)

    def test_logger_text_format_output(self):
        """Test CustomLogger text format output."""
        logger = CustomLogger(name='fbloggsfunction', format='text')
        
        # Capture the output
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Protocol problem: connection reset')
        output = stream.getvalue().strip()
        
        # Text format should include date, time, name, and message
        self.assertIn('fbloggsfunction', output)
        self.assertIn('Protocol problem: connection reset', output)
        # Should have date and time
        self.assertRegex(output, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    def test_logger_json_format_output(self):
        """Test CustomLogger JSON format output."""
        logger = CustomLogger(name='fbloggsfunction', format='json')
        
        # Capture the output
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Protocol problem: connection reset')
        output = stream.getvalue().strip()
        
        log_data = json.loads(output)
        self.assertIn('date', log_data)
        self.assertIn('time', log_data)
        self.assertEqual(log_data['name'], 'fbloggsfunction')
        self.assertEqual(log_data['message'], 'Protocol problem: connection reset')

    def test_logger_date_format(self):
        """Test CustomLogger date format is yyyy-mm-dd."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Test')
        output = stream.getvalue().strip()
        
        date_part = output.split()[0]
        # Check format yyyy-mm-dd
        self.assertRegex(date_part, r'\d{4}-\d{2}-\d{2}')

    def test_logger_time_format(self):
        """Test CustomLogger time format is hh:mm:ss."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Test')
        output = stream.getvalue().strip()
        
        time_part = output.split()[1]
        # Check format hh:mm:ss
        self.assertRegex(time_part, r'\d{2}:\d{2}:\d{2}')

    def test_logger_info_level(self):
        """Test CustomLogger info level."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Info message')
        output = stream.getvalue().strip()
        self.assertIn('Info message', output)

    def test_logger_debug_level(self):
        """Test CustomLogger debug level."""
        logger = CustomLogger(name='test_logger', level=logging.DEBUG, format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.debug('Debug message')
        output = stream.getvalue().strip()
        self.assertIn('Debug message', output)

    def test_logger_warning_level(self):
        """Test CustomLogger warning level."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.warning('Warning message')
        output = stream.getvalue().strip()
        self.assertIn('Warning message', output)

    def test_logger_error_level(self):
        """Test CustomLogger error level."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.error('Error message')
        output = stream.getvalue().strip()
        self.assertIn('Error message', output)

    def test_logger_critical_level(self):
        """Test CustomLogger critical level."""
        logger = CustomLogger(name='test_logger', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.critical('Critical message')
        output = stream.getvalue().strip()
        self.assertIn('Critical message', output)

    def test_logger_name_property(self):
        """Test CustomLogger name property."""
        logger = CustomLogger(name='my_logger')
        self.assertEqual(logger.name, 'my_logger')


class TestGetLogger(unittest.TestCase):
    """Test cases for get_logger function."""

    def setUp(self):
        """Set up test fixtures."""
        for logger_name in list(logging.Logger.manager.loggerDict):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

    def test_get_logger_default(self):
        """Test get_logger with default parameters."""
        logger = get_logger('test_logger')
        self.assertIsInstance(logger, CustomLogger)
        self.assertEqual(logger.name, 'test_logger')

    def test_get_logger_custom_level(self):
        """Test get_logger with custom level."""
        logger = get_logger('test_logger', level=logging.DEBUG)
        self.assertEqual(logger._logger.level, logging.DEBUG)

    def test_get_logger_custom_format(self):
        """Test get_logger with custom format."""
        logger_text = get_logger('test_text', format='text')
        logger_json = get_logger('test_json', format='json')
        
        self.assertEqual(logger_text._logger.handlers[0].formatter.output_format, 'text')
        self.assertEqual(logger_json._logger.handlers[0].formatter.output_format, 'json')


class TestLoggerIntegration(unittest.TestCase):
    """Integration tests for the custom logger."""

    def setUp(self):
        """Set up test fixtures."""
        for logger_name in list(logging.Logger.manager.loggerDict):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

    def test_text_format_output_structure(self):
        """Test text format output has correct structure."""
        logger = CustomLogger(name='fbloggsfunction', format='text')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Protocol problem: connection reset')
        output = stream.getvalue().strip()
        
        # Expected: YYYY-MM-DD HH:MM:SS name [funcName] message
        self.assertRegex(output, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} fbloggsfunction .* Protocol problem: connection reset')

    def test_json_format_valid_json(self):
        """Test JSON format produces valid JSON."""
        logger = CustomLogger(name='TestApp', format='json')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Test message')
        output = stream.getvalue().strip()
        
        # Should be valid JSON
        log_data = json.loads(output)
        self.assertIsInstance(log_data, dict)

    def test_json_format_contains_all_fields(self):
        """Test JSON format contains all required fields."""
        logger = CustomLogger(name='TestApp', format='json')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        logger.info('Test message')
        output = stream.getvalue().strip()
        
        log_data = json.loads(output)
        
        self.assertIn('date', log_data)
        self.assertIn('time', log_data)
        self.assertEqual(log_data['name'], 'TestApp')
        self.assertEqual(log_data['message'], 'Test message')

    def test_logger_with_method_call(self):
        """Test logger when called from a method."""
        logger = CustomLogger(name='AppLogger', format='json')
        
        handler = logger._logger.handlers[0]
        stream = StringIO()
        handler.stream = stream
        
        # Simulate a method call
        def my_method():
            logger.info('Method message')
        
        my_method()
        output = stream.getvalue().strip()
        
        log_data = json.loads(output)
        self.assertEqual(log_data['funcName'], 'my_method')
        self.assertIn('Method message', log_data['message'])


if __name__ == '__main__':
    unittest.main()
