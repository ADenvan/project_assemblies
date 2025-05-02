import os
import sys

python_path = os.path.dirname(sys.executable)

python_version = sys.version

# В терминал .\main.py
print(f'ПИТЬ К ИНТЕРПРЕТАТОРУ {python_path}. ВЕРСИЯ {python_version}')
