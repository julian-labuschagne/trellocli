import argparse
import yaml
from os.path import expanduser
from trello import TrelloClient

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

if __name__ == "__main__":
    cfg = get_config()
    client = create_trello_object(cfg)

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true", help="List Boards")
    parser.add_argument("-b", "--board", help="Trello Board")
    args = parser.parse_args()

    if args.list:
        """List of all the Trello Boards"""
        boards = client.list_boards()

        """Print information from Boards"""
        for board in boards:
            print(board.id)
            print(board.name.decode('utf-8'))

            for member in board.get_members():
                print('\t{}'.format(member.full_name.decode('utf-8')))
    if args.board:
        print("Chosen board")
