
### how to run
you can run this application with following commands
```shell script
cd ../venv/Scripts
activate.bat

cd ../../app
py manage.py runserver
```






### code hints
```python
# check user
def view_set(request):
    if request.user is not "Anonymous":
        pass

```