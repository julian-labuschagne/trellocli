import yaml
from os.path import expanduser
from trello import TrelloClient

"""Load trello user credentials from yaml file"""
home = expanduser("~")
with open('{}/.trello-config.yml'.format(home), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

"""Create a new TrelloClient Object using the proper user credentials"""
client = TrelloClient(
api_key=cfg['trello']['api_key'],
api_secret=cfg['trello']['api_secret'],
token=cfg['trello']['token'],
token_secret=cfg['trello']['token_secret']
)

"""Get a list of all the Trello Boards"""
boards = client.list_boards()

"""Print information from Boards"""
for board in boards:
    print(board.id)
    print(board.name.decode('utf-8'))

    for member in board.get_members():
        print('\t{}'.format(member.full_name.decode('utf-8')))
