# pyrst

The Python wrapper to the Birst API.
- No token repetition: once you obtain a token, Pyrst will manage it for you
until you tell it to stop.
- Super easy querying
- Even easier output using handlers

# How to install

Until we release this project to PyPI, the best way to install is:

```
git clone --recursive https://github.com/rbonedata/pyrst.git
python setup.py install
```

On OS X and Linux, unless you're installing in a venv, you might need to run
the install scripts as a privileged user (`sudo`).

# How to use

## General usage

### Importing the client and create a client object

You can store configuration in a config file - a template of the config file is
under the `pyrst` folder. You can name the config file anything you want. To
keep the password somewhat safe, use `base64` encoding and set the
`password_is_encrypted` flag to `True`.

```python
from pyrst.client import BirstClient

client = BirstClient(configfile='pyrst/config.yaml')
```

Alternatively, you can manually create the client:

```python
from pyrst.client import BirstClient

client = BirstClient(user = "MyUsername",
                     password = "MyPassword")
```

### Login

```python
client.login()
```

```
You have been successfully logged in, DOMAIN\Username.
Your token is: 9b4081fa4b9f3d8d15f77271b7e83902
```

### Logout

Once you're done, simply use `client.logout()` to log out.


## Querying

To query a space, use `executequery()`. Before querying, it makes sense to
import the handler that you want to use to display the data, if any:

```python
from pyrst.handlers import DfHandler
```

Now you can use it in your query:

```python
table = executequery(space = "12345678-abcd-9012-efab-345678901234",
                     query = "SELECT [# sales_total] from [ALL]",
                     handler = DfHandler)
```


# Development roadmap

The current functionality doesn't do much beyond querying, but we'll be
steadily developing `Pyrst`'s capabilities. In particular, multipart querying
and more handlers will be implemented soon.

Current priorities are:
- better handlers,
- better query handling,
- JSON output,
- tests,
- documentation,
- more functionality.

# Credits

Written by Chris von Csefalvay with the generous support of RB.