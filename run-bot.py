from src.telegram.bot import main_loop
import sys

while True:
        try:
            main_loop()
        except KeyboardInterrupt:
            print('\nExiting by user request.\n')
            sys.exit(0)
