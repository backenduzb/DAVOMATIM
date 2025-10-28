#!/usr/bin/env python
import os
import sys
import asyncio

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc

    # 🟢 Botni alohida ishga tushirish
    if 'runbot' in sys.argv:
        from bot.main import bot_main
        asyncio.run(bot_main())
        return  # ❗ Muhim: Django command systemga qaytmasin
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
