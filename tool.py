
class FlashCards:

    msg_question = 'Question:'
    msg_need_answer = 'Please press "y" to see the answer or press "n" to skip:'
    msg_answer = 'Answer:'
    msg_no_cards = 'There is no flashcard to practice!'

    def __init__(self):
        self.cards = {}

    def add_card(self):
        print(self.msg_question)
        question = input()
        while question == ' ' or not question:
            print(self.msg_question)
            question = input()

        print(self.msg_answer)
        answer = input()
        while answer == ' ' or not answer:
            print(self.msg_answer)
            answer = input()
        self.cards[question] = answer
        print()

    def practice_card(self):
        if not self.cards:
            print(self.msg_no_cards)
        else:
            for question in self.cards:
                print(self.msg_question, question)
                print(self.msg_need_answer)
                if input() == 'y':
                    print()
                    print(self.msg_answer, self.cards[question])
                print()


class Menu:

    flashCards = FlashCards()

    msg_add_new_cards = '1. Add flashcards'
    msg_add_new_card = '1. Add a new flashcard'
    msg_exit_1 = '3. Exit'
    msg_exit_2 = '2. Exit'
    msg_practice = '2. Practice flashcards'
    msg_bye = 'Bye!'

    def __init__(self, stage):
        self.menu_stage = stage

    def print_menu(self):
        if self.menu_stage == 1:  # start menu
            while not self.print_menu_stage_1():
                pass
        elif self.menu_stage == 2:  # add card menu
            while not self.print_menu_stage_2():
                pass
        elif self.menu_stage == 3:  # practice menu
            self.print_menu_stage_3()
        #elif self.menu_stage == 4:  # exit
        #    print(self.msg_bye)

        if self.menu_stage != 4:
            self.print_menu()
        else:
            print(self.msg_bye)

    def print_menu_stage_1(self):
        print(self.msg_add_new_cards)
        print(self.msg_practice)
        print(self.msg_exit_1)

        # check option
        option = input()
        print()
        # noinspection PyBroadException
        try:
            option = int(option)
        except Exception as error:
            print(f'{option} is not an option')
            return False

        if option == 1:
            self.menu_stage = 2
        elif option == 2:
            self.menu_stage = 3
        elif option == 3:
            self.menu_stage = 4
        else:
            print(f'{option} is not an option')
            return False
        return True

    def print_menu_stage_2(self):
        print(self.msg_add_new_card)
        print(self.msg_exit_2)

        option = input()
        try:
            option = int(option)
        except Exception as error:
            print(f'{option} is not an option')
            return False

        print()

        if option == 1:
            self.flashCards.add_card()
        elif option == 2:
            self.menu_stage = 1
        else:
            print(f'{option} is not an option')
            return False
        return True

    def print_menu_stage_3(self):
        self.flashCards.practice_card()
        self.menu_stage = 1


if __name__ == '__main__':
    menu = Menu(1)
    menu.print_menu()

