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


    # board = trello.get_board('Test Board')
    # todo_list = trello.get_list(board, 'Todo')
    # member = trello.get_member(board, 'Julian Labuschagne')
    #
    # # Prepare a date
    # date_time_str = '2019-03-21 13:00:00.000000'
    # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    #
    # # Prepare a list of Todo items
    # list_items = {
    #     'Item 01',
    #     'Item 02',
    #     'Item 03'
    # }
    #
    # # Create a new card
    # new_card = todo_list.add_card(name='TEST CARD PyYaml', desc='This is the card description')
    # new_card.set_due(date_time_obj)
    # new_card.add_member(member)
    # new_card.add_checklist('Todo', list_items)
    #
    # print('Board ID  : {id}'.format(id=board.id))
    # print('List ID   : {id}'.format(id=todo_list.id))
    # print('Member ID : {id}'.format(id=member.id))
    # print('Card ID   : {id}'.format(id=new_card.id))
    #
    # trello.display_cards(todo_list)

    # Create a new instance of argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='mode')

    add_card_parser = subparsers.add_parser('add-card', help='Add card parser help')
    add_card_parser.add_argument('--board')
    add_card_parser.add_argument('--list')
    add_card_parser.add_argument('--name')
    add_card_parser.add_argument('--due')

    list_card_parser = subparsers.add_parser('list-cards', help='Add list card parser help')
    list_card_parser.add_argument('--board')
    list_card_parser.add_argument('--list')


    # parser.add_argument('addcard', metavar='add-card', help='Create a new trello card')
    # parser.add_argument('listcards', metavar='list-cards', help='List cards')

    args = parser.parse_args()
    print(args.mode)

    if args.mode == 'list-cards':
        # print(args.board)
        # print(args.list)

        board = trello.get_board(args.board)
        todo_list = trello.get_list(board, args.list)
        trello.display_cards(todo_list)

    if args.mode == 'add-card':
        board = trello.get_board(args.board)
        todo_list = trello.get_list(board, args.list)

        # Create a new card
        new_card = todo_list.add_card(name=args.name, desc='This is the card description')

        if args.due:
            # Prepare a date
            date_time_str = args.due
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
            new_card.set_due(date_time_obj)

        # new_card.add_member(member)
        # new_card.add_checklist('Todo', list_items)
