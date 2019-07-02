import sys

from .models import Organization, Ticket, User
from .views import InvalidSearchTermException, Search


class AppController(object):
    def __init__(self):
        self.input = ""
        self.view = AppView()

    def run(self):
        self.check_data_loaded()
        self.show_main_menu()

    def check_data_loaded(self):
        if (
                Organization.objects.count() == 0 and
                User.objects.count() == 0 and
                Ticket.objects.count() == 0
        ):
            print(
                '\nExiting search as data is not loaded.\n\nLoad data by running the below command:\n'
                'python manage.py load_data\n'
            )
            sys.exit()

    def show_main_menu(self):
        self.view.display_start_message()
        self.view.display_menu()
        while True:
            self.get_input()
            if self.input == "menu":
                self.view.display_menu()
            elif self.input == '1':
                self.process_search_options()
            elif self.input == '2':
                self.display_searchable_fields()
            elif self.input == 'quit':
                sys.exit(self.view.display_quit_message())
            else:
                self.view.display_message(
                    "\nInvalid input, please enter a valid command. To view command options type 'menu'."
                )
            self.input = ""

    def get_input(self):
        self.input = input()

    def process_search_options(self):
        self.view.display_search_options_message()
        while True:
            self.get_input()
            self.check_for_exit(self.input)
            if self.input == '1':
                self.search_entity = 'Users'
                break
            elif self.input == '2':
                self.search_entity = 'Tickets'
                break
            elif self.input == '3':
                self.search_entity = 'Organizations'
                break
            else:
                self.view.display_message(
                    "\nInvalid input, please enter a valid option 1, 2, 3 to continue search or 'quit' to exit"
                )
                continue

        self.process_search_params()
        self.view.display_menu()
        return

    def process_search_params(self):
        while True:
            self.search_term = input('\nEnter search term:\n')
            self.check_for_exit(self.search_term)
            if not self.search_term:
                print('Search term cannot be empty.')
                continue

            self.search_value = input('\nEnter search value:\n')
            self.check_for_exit(self.search_value)
            break
        self.search_models()

    def search_models(self):
        self.search = Search(self.search_term, self.search_value)
        if self.search_entity == 'Users':
            self.search_users()
        elif self.search_entity == 'Tickets':
            self.search_tickets()
        elif self.search_entity == 'Organizations':
            self.search_organizations()

    def search_organizations(self):
        print(f'\nSearching organizations for {self.search_term} with a value of {self.search_value} .....')
        try:
            qs = self.search.search_organizations()
        except InvalidSearchTermException as e:
            print(f'\n{e}\n')
            self.view.display_menu()
            return

        if not qs:
            print(f'\nNo results found for search term {self.search_term} and search value {self.search_value}')
            self.view.display_menu()
        else:
            for organization in qs:
                print(organization)
        return

    def search_tickets(self):
        print(f'\nSearching tickets for {self.search_term} with a value of {self.search_value} .....')
        try:
            qs = self.search.search_tickets()
        except InvalidSearchTermException as e:
            print(f'\n{e}\n')
            return
        
        if not qs:
            print(f'\nNo results found for search term {self.search_term} and search value {self.search_value}')
        else:
            for ticket in qs:
                print(ticket)
        return

    def search_users(self):
        print(f'\nSearching users for {self.search_term} with a value of {self.search_value} .....')
        try:
            qs = self.search.search_users()
        except InvalidSearchTermException as e:
            print(f'\n{e}\n')
            return
        
        if not qs:
            print(f'\nNo results found for search term {self.search_term} and search value {self.search_value}')
        else:
            for user in qs:
                print(user)
        return

    def display_searchable_fields(self):
        self.display_users_searchable_fields()
        self.display_tickets_searchable_fields()
        self.display_organizations_searchable_fields()
        self.view.display_menu()

    def display_users_searchable_fields(self):
        print('\n-----------------------------------------------------------')
        print('Search Users with:\n')
        for f in User._meta.fields:
            print(f'{f.name}')

    def display_tickets_searchable_fields(self):
        print('\n-----------------------------------------------------------')
        print('Search Tickets with:\n')
        for f in Ticket._meta.fields:
            print(f'{f.name}')

    def display_organizations_searchable_fields(self):
        print('\n-----------------------------------------------------------')
        print('Search Organizations with:\n')
        for f in Organization._meta.fields:
            print(f'{f.name}')
        print('\n')

    def check_for_exit(self, user_input):
        if user_input == 'quit':
            sys.exit(self.view.display_quit_message())


class AppView(object):
    def display_start_message(self):
        print("\nWelcome to Zendesk Search")
        print(
            "\nSelect from the below options. Type 'quit' to exit the application, "
            "'menu' to display the main menu at any time."
        )
        

    def display_message(self, message):
        print(message)

    def display_menu(self):
        print("\nSearch options:")
        print("\t* Enter 1 to search Zendesk.")
        print("\t* Enter 2 to view a list of searchable fields.")
        print("\t* Enter 'quit' to exit application.")
        print("\t* Enter 'menu' to display menu.")
        print("\nEnter your choice: ")

    def display_search_options_message(self):
        print("\nSelect 1) Users or 2) Tickets or 3) Organizations")

    def display_quit_message(self):
        print("\nExit Zendesk Search successful...\n")
