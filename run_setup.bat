@echo off
chcp 65001

cd /d %~dp0

REM 创建虚拟环境
python -m venv venv

REM 启动虚拟环境并安装依赖
call venv\Scripts\activate
pip install -r requirements.txt

echo ✅ QTXD_PartySummarizer 环境初始化完成！
pause
