ECHO Begin to install Python...
start /wait .\package\python-2.7.10.msi /QB
ECHO.

set PATH=%PATH%;C:\Python27\;C:\Python27\Scripts;

ECHO Begin to install dependence...
pip install .\package\Django-1.11.2-py2.py3-none-any.whl
pip install .\package\MarkupSafe-0.23-cp27-none-win32.whl
pip install .\package\Mako-1.0.3-py2.py3-none-any.whl
pip install .\package\xlrd-0.9.4-py2.py3-none-any.whl
pip install .\package\xlwt-1.0.0-py2.py3-none-any.whl
pip install .\package\Pillow-3.0.0-cp27-none-win32.whl
ECHO.