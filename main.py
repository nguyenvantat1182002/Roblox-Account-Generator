from models import rand_account
from roblox import Roblox

r = Roblox()

account = rand_account()
r.sign_up(account)


print(account.username, account.password)
