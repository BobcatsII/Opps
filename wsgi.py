import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from opps import create_app

#使用工厂函数创建程序实例,传入配置名
app = create_app('production')
