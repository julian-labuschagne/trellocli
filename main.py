import argparse
import yaml
import datetime
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
        """ Get the board from the board name """
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

    def display_cards(self, trello_list):
        cards = trello_list.list_cards()
        for card in cards:
            print(card.name)

if __name__ == "__main__":

    trello = TrelloCli()

    board = trello.get_board('Test Board')
    todo_list = trello.get_list(board, 'Todo')
    member = trello.get_member(board, 'Julian Labuschagne')

    # Prepare a date
    date_time_str = '2019-03-21 13:00:00.000000'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    # Prepare a list of Todo items
    list_items = {
        'Item 01',
        'Item 02',
        'Item 03'
    }

    # Create a new card
    new_card = todo_list.add_card(name='TEST CARD PyYaml', desc='This is the card description')
    new_card.set_due(date_time_obj)
    new_card.add_member(member)
    new_card.add_checklist('Todo', list_items)

    print('Board ID  : {id}'.format(id=board.id))
    print('List ID   : {id}'.format(id=todo_list.id))
    print('Member ID : {id}'.format(id=member.id))
    print('Card ID   : {id}'.format(id=new_card.id))

    trello.display_cards(todo_list)
