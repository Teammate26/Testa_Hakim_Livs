GIT BASH

```
python -m venv venv
source venv/Scripts/activate

pip install -r requirements.txt
```
Create a .env file and enter the credentials, then install it
```
ADMIN_USERNAME=
ADMIN_PASSWORD=
```
Install Playwright if new PC
```
playwright install
```
Run test_hakim_livs.py to check if everything is working
```
pytest --headed --slowmo 1000 test_hakim_livs.py
```
