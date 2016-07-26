from argparse import ArgumentParser
from os import environ, path
from sys import exit

from jinja2 import Environment, FileSystemLoader
from trello import TrelloClient
from mistune import Markdown


def main():
    parser = ArgumentParser(description='Generate a status page from a Trello '
                                        'board')
    parser.add_argument('-k', '--key', dest='key',
                        default=environ.get('TRELLO_KEY'),
                        help='Trello API key')
    parser.add_argument('-s', '--secret', dest='secret',
                        default=environ.get('TRELLO_SECRET'),
                        help='Trello API secret')
    parser.add_argument('-t', '--token', dest='token',
                        default=environ.get('TRELLO_TOKEN'),
                        help='Trello API auth token')
    parser.add_argument('-S', '--token-secret', dest='token_secret',
                        default=environ.get('TRELLO_TOKEN'),
                        help='Trello API auth token secret')
    parser.add_argument('-b', '--board-id', dest='board',
                        default=environ.get('TRELLO_BOARD_ID'),
                        help='Trello board ID')
    parser.add_argument('output_path', help='Path to output rendered HTML to')
    args = parser.parse_args()

    client = TrelloClient(
        api_key=args.key,
        api_secret=args.secret,
        token=args.token,
        token_secret=args.token_secret)

    markdown = Markdown()
    board = client.get_board(args.board)
    labels = board.get_labels()
    services = [l for l in labels if not l.name.startswith('status:')]
    service_ids = [s.id for s in services]
    status_types = [l for l in labels if l not in services]
    lists = board.open_lists()
    incidents = []
    panels = {}
    systems = {}

    for card_list in lists:
        for card in card_list.list_cards():
            severity = ''
            for label in card.labels:
                if not label.name.startswith('status:'):
                    continue

                severity = label.name.lstrip('status:').lstrip()
                if label.color == 'red':
                    break
            card.severity = severity


            card_services = [l.name for l in card.labels if l.id in service_ids]
            if card_list.name.lower() == 'fixed':
                card.closed = True
            else:
                if card.severity not in panels:
                    panels[card.severity] = []
                panels[card.severity] += card_services

                for service in card_services:
                    if service not in systems:
                        systems[service] = {'status': card_list.name,
                                            'severity': card.severity}

            card.html_desc = markdown(card.desc)

            comments = card.fetch_comments(force=True)
            for comment in comments:
                comment['html_desc'] = markdown(comment['data']['text'])

            card.parsed_comments = comments

            incidents.append(card)

    for service in services:
        if service.name not in systems:
            systems[service.name] = {'status': 'Operational', 'severity': ''}


    env = Environment(loader=FileSystemLoader(
        path.join(path.dirname(__file__), 'templates')))
    template = env.get_template('template.html')
    with open(args.output_path, 'w+') as f:
        f.write(template.render(incidents=incidents, panels=panels,
                                systems=systems))

    print('Status page written to {}'.format(args.output_path))
    return 0


if __name__ == '__main__':
    exit(main())
