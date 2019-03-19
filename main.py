import argparse
import yaml
from os.path import expanduser
from trello import TrelloClient

class TrelloCli:

    """ Load Trello api keys from yaml file"""
    def __init__(self, file='config.yml'):
        with open(file, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                self.__key = config('key')
                self.__token = config('token')
                self.__client = TrelloClient(
                    api_key = config('key'),
                    api_secret = config('secret')
                )
            except:
                yaml.YAMLError as exc:
                    print(exc)

def get_config():
    """Load trello user credentials from yaml file"""
    home = expanduser("~")
    with open('{}/.trello-config.yml'.format(home), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        return cfg

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
    cfg = get_config()
    client = create_trello_object(cfg)

    """Create the parser object and add arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true", help="List Boards")
    parser.add_argument("-c", "--create", action="store_true", help="List Boards")
    parser.add_argument("-B", "--board", help="Trello Board Name")
    parser.add_argument("-C", "--card", help="Trello Card Name")
    parser.add_argument("-L", "--list-name", help="Trello List Name")
    args = parser.parse_args()

    if args.list:
        """List of all the Trello Boards"""
        boards = client.list_boards()

        """Print Board information"""
        for board in boards:
            print("{}\t{}".format(board.id, board.name.decode('utf-8')))

    if args.create:
        if args.card != "":
            print("Create a new card")
            #print(dir(get_trello_list(client, args.board, args.list_name)))
            new_card = get_trello_list(client, args.board, args.list_name).add_card("New Card Created By Python Script", desc="This card was created by a Python Script called trellocli https://github.com/julian-labuschagne/trellocli")
            print(new_card)
