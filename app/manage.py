import argparse

import uvicorn
from dotenv import load_dotenv

from app.core.config import settings

# init parser
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--runserver', action='store_true')
parser.add_argument('--reload', action='store_true')
args = parser.parse_args()

load_dotenv()


def main():
    if args.runserver:
        uvicorn.run(
            'app.main:app',
            port=settings.SERVER_PORT,
            log_level='info',
            host=settings.SERVER_HOST,
            reload=args.reload
        )


if __name__ == '__main__':
    main()
