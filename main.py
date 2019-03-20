import argparse
import yaml
from os.path import expanduser
from trello import TrelloClient

class TrelloCli:

    def __init__(self, file='config.yml'):
        """ Load Trello api keys from yaml file"""
        with open(file, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                self.__client = TrelloClient(
                    api_key = config['key'],
                    api_secret = config['token']
                )
            except yaml.YAMLError as exc:
                    print(exc)

    def get_board(self, board_name):
        """ Get the board id from the board name """
        boards = self.__client.list_boards()
        for board in boards:
            if board.name == board_name:
                return self.__client.get_board(board.id)

    def get_list(self, board, list_name):
        lists = board.all_lists()
        for list in lists:
            if list.name == list_name:
                return board.get_list(list.id)

    def get_member(self, board, member_name):
        members = board.all_members()
        for member in members:
            if member.full_name == member_name:
                return member



def create_trello_object(cfg):
    """Create a new TrelloClient Object using the proper user credentials"""
    client = TrelloClient(
        api_key=cfg['trello']['api_key'],
        api_secret=cfg['trello']['api_secret'],
        token=cfg['trello']['token'],
        token_secret=cfg['trello']['token_secret']
    )
    return client

def get_trello_list(client, board_name, list_name):
    for board in client.list_boards():
        if board_name == board.name.decode('utf-8'):
            print(board.name.decode('utf-8'))
            for board_list in board.all_lists():
                return board_list

if __name__ == "__main__":

    trello = TrelloCli()

    board = trello.get_board('Test Board')
    todo_list = trello.get_list(board, 'Todo')
    member = trello.get_member(board, 'Julian Labuschagne')
    new_card = todo_list.add_card(name='TEST CARD PyYaml', desc='This is the card description')

    print('Board ID  : {id}'.format(id=board.id))
    print('List ID   : {id}'.format(id=todo_list.id))
    print('Member ID : {id}'.format(id=member.id))
    print('Card ID   : {id}'.format(id=new_card.id))
