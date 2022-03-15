from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class FirstLeitnerLayer(Base):
    __tablename__ = 'firstTable'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


class SecondLeitnerLayer(Base):
    __tablename__ = 'secondTable'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


class ThirdLeitnerLayer(Base):
    __tablename__ = 'thirdTable'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)


Base.metadata.create_all(engine)


class FlashCards:
    firstTable = session.query(FirstLeitnerLayer).all()
    secondTable = session.query(SecondLeitnerLayer).all()
    thirdTable = session.query(ThirdLeitnerLayer).all()

    msg_current_question = 'current question:'
    msg_new_question = 'please write a new question:'
    msg_current_answer = 'current answer:'
    msg_new_answer = 'please write a new answer:'

    @staticmethod
    def add_card(question, answer):
        new_data = FirstLeitnerLayer(question=question, answer=answer)
        session.add(new_data)
        session.commit()
        print()

    @staticmethod
    def delete_element(table_name, element):
        session.query(table_name).filter(table_name.id == element.id).delete()
        session.commit()

    def edit_element(self, table_name, element):
        current_filter = session.query(table_name).filter(table_name.id == element.id)
        print(self.msg_current_question, element.question)
        print(self.msg_new_question)
        current_filter.update({"question": input()})
        print(self.msg_current_answer, element.answer)
        print(self.msg_new_answer)
        current_filter.update({"answer": input()})
        session.commit()

    def update_tables(self):
        self.firstTable = session.query(FirstLeitnerLayer).all()
        self.secondTable = session.query(SecondLeitnerLayer).all()
        self.thirdTable = session.query(ThirdLeitnerLayer).all()


class Menu:

    flashCards = FlashCards()
    currentSession = 0

    msg_add_new_cards = '1. Add flashcards'
    msg_add_new_card = '1. Add a new flashcard'
    msg_exit_1 = '3. Exit'
    msg_exit_2 = '2. Exit'
    msg_practice = '2. Practice flashcards'
    msg_bye = 'Bye!'
    msg_question = 'Question:'
    msg_need_answer = 'press "y" to see the answer:'
    msg_answer = 'Answer:'
    msg_no_cards = 'There is no flashcard to practice!'
    msg_update = 'press "u" to update:'
    msg_skip = 'press "n" to skip:'
    msg_delete = 'press "d" to delete the flashcard:'
    msg_edit = 'press "e" to edit the flashcard:'
    msg_is_correct = 'press "y" if your answer is correct:'
    msg_is_wrong = 'press "n" if your answer is wrong:'

    def __init__(self, stage):
        self.menu_stage = stage

    def print_menu(self):
        if self.menu_stage == 1:  # start menu
            while not self.main_menu():
                pass
        elif self.menu_stage == 2:  # add card menu
            while not self.add_new_card_menu():
                pass
        elif self.menu_stage == 3:  # practice menu
            self.practice_menu()

        if self.menu_stage != 4:
            self.print_menu()
        else:
            print(self.msg_bye)

    def main_menu(self):
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

    def card_info_input(self):
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
        return question, answer

    def add_new_card_menu(self):
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
            self.flashCards.add_card(*self.card_info_input())
        elif option == 2:
            self.menu_stage = 1
        else:
            print(f'{option} is not an option')
            return False
        return True

    def practice_menu(self):
        self.question_menu()
        self.menu_stage = 1

    @staticmethod
    def define_table(current_table):
        if current_table == 1:
            return FirstLeitnerLayer
        elif current_table == 2:
            return SecondLeitnerLayer
        elif current_table == 3:
            return ThirdLeitnerLayer
        return None

    def is_right(self, current_table, element):
        print(self.msg_is_correct)
        print(self.msg_is_wrong)
        option = input()
        if option == 'y':
            table_name = self.define_table(current_table)
            self.flashCards.delete_element(table_name, element)
            if current_table + 1 <= 3:
                table_name = self.define_table(current_table + 1)
                self.flashCards.edit_element(table_name, element)
        elif option == 'n':
            if current_table > 1:
                table_name = self.define_table(current_table)
                self.flashCards.delete_element(table_name, element)
                table_name = self.define_table(1)
                self.flashCards.edit_element(table_name, element)
        else:
            print(f'{option} is not an option')
            return False
        return True

    def que_option(self, element, current_table):
        print(self.msg_question, element.question)
        print(self.msg_need_answer)
        print(self.msg_skip)
        print(self.msg_update)

        option = input()

        if option == 'y':
            print()
            print(self.msg_answer, element.answer)
            while not self.is_right(current_table, element):
                pass
        elif option == 'n':
            pass
        elif option == 'u':
            print(self.msg_delete)
            print(self.msg_edit)
            while not self.update_menu(self.define_table(current_table), element):
                pass
        else:
            print(f'{option} is not an option')
            return False
        return True

    def run_trough_list(self, local_list, list_number):
        if not local_list:
            return False
        else:
            for element in local_list:
                while not self.que_option(element, list_number):
                    pass
            return True

    def question_menu(self):
        self.flashCards.update_tables()
        is_empty = False
        if self.currentSession >= 0:
            is_empty = self.run_trough_list(self.flashCards.firstTable, 1)
        if self.currentSession >= 1:
            is_empty = self.run_trough_list(self.flashCards.secondTable, 2)
        if self.currentSession >= 2:
            is_empty = self.run_trough_list(self.flashCards.thirdTable, 3)

        if not is_empty:
            print(self.msg_no_cards)

        self.currentSession += 1
        self.currentSession %= 3

    def update_menu(self, table_name, element):
        option = input()
        if option == 'd':
            self.flashCards.delete_element(table_name, element)
        elif option == 'e':
            self.flashCards.edit_element(table_name, element)
        else:
            print(f'{option} is not an option')
            return False
        return True


if __name__ == '__main__':
    menu = Menu(1)
    menu.print_menu()
