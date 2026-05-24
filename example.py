from custom_logger import CustomLogger


class ExampleClass:
    def __init__(self, name: str, format: str = 'text'):
        self.logger = CustomLogger(name=name, format=format)

    def sample_method(self):
        self.logger.info('Protocol problem: connection reset')


if __name__ == '__main__':
    # Example 1: Text format
    print('=== Text Format ===')
    logger_text = CustomLogger(name='fbloggsfunction', format='text')
    logger_text.info('Protocol problem: connection reset')

    print()

    # Example 2: JSON format
    print('=== JSON Format ===')
    logger_json = CustomLogger(name='fbloggsfunction', format='json')
    logger_json.info('Protocol problem: connection reset')

    print()

    # Example 3: Text format with class
    print('=== Text Format with Class ===')
    example_text = ExampleClass('MyApp', format='text')
    example_text.sample_method()

    print()

    # Example 4: JSON format with class
    print('=== JSON Format with Class ===')
    example_json = ExampleClass('MyApp', format='json')
    example_json.sample_method()
