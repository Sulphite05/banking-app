from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime, date
from csv import reader, writer
from os import listdir


# all the classes are inherited from some user-defined or external parent class displaying the use of OOP to
# implement GUI throughout our program


class Manager(ScreenManager):
    pass  # implementation of class is done in the .kv file


class SignUpInterface(Screen):
    def signup_btn(self, first_name: TextInput, last_name: TextInput, address: TextInput, username: TextInput,
                   password: TextInput):
        # example of weaker association(passing instance properties to another class' instance method)
        if first_name.text != "" and last_name.text != "" and address.text != "" and password.text \
                != "" and username.text != "":

            with open('user_data.csv', 'r') as csvfile:
                csv_reader = reader(csvfile)
                append_in_file = True
                for row in csv_reader:  # csv reader gets rows in the form of lists
                    if row[3] == username.text:
                        append_in_file = False

            if append_in_file:
                with open('user_data.csv', 'a') as csvfile_r:
                    writer(csvfile_r).writerow([first_name.text, last_name.text, address.text,  # saves user info
                                                username.text, password.text])
                    CreateAccountInterface().receiveData(username.text)  # another example of weaker association
                    self.manager.current = 'Create Account'
                    first_name.text = ""
                    last_name.text = ""
                    address.text = ""
                    password.text = ""
                    username.text = ""

            else:
                l1 = Label(text='Username has already been taken.\nPlease use a new username', color='red',
                           halign='center', valign='middle')
                popup = Popup(title='Warning', content=l1, title_color='red', separator_color='red')
                popup.size_hint = 0.4, 0.2
                popup.open()

        else:
            l2 = Label(text='Please fill in all the entries!', color='red', halign='center', valign='middle')
            popup = Popup(title='Warning', content=l2, title_color='red', separator_color='red')
            popup.size_hint = 0.4, 0.2
            popup.open()


class CreateAccountInterface(Screen):
    types_of_accounts = []

    @classmethod
    def receiveData(cls, username):
        cls.userData = username

    def createAccBtn(self, t1: ToggleButton, t2: ToggleButton, t3: ToggleButton):

        time_now = datetime.now().strftime("%H:%M:%S")
        date_now = datetime.now().strftime("%d-%m-%Y")

        if t1.state == 'down':
            with open(f'CheckingAccounts/{self.userData}.csv', 'a') as f:
                writer(f).writerow([1000, 1000, 0, 10000, time_now, date_now])
                # balance, deposited, withdrawn, overdraft, time of transaction, date of transaction
                self.types_of_accounts.append('Checking_Account')

        if t2.state == 'down':
            with open(f'SavingAccounts/{self.userData}.csv', 'a') as f:
                writer(f).writerow([1000, 1000, 0, time_now, date_now + ' credit'])
                # savings, deposited, withdrawn, date of transaction
                self.types_of_accounts.append('Savings_Account')

        if t3.state == 'down':
            LoanAccountInterface.loan_acquisition(self, self.userData)
            self.types_of_accounts.append('Loan_Account')

        if t1.state != 'down' and t2.state != 'down' and t3.state != 'down':
            with open(f'BasicAccounts/{self.userData}.csv', 'a') as f:
                writer(f).writerow([1000, 1000, 0, time_now, date_now])
                # balance, deposited, withdrawn, date/time of transaction

        with open('user_accounts.csv', 'a') as f:
            writer(f).writerow([self.userData, self.types_of_accounts])
            self.types_of_accounts = []

    def display(self, t1: ToggleButton, t2: ToggleButton, t3: ToggleButton):
        if t1.state == 'normal' and t2.state == 'normal' and t3.state == 'down':
            pass

        else:
            popup = Popup(title='MTABank Account Status', content=Label(text='Account(s) successfully created with '
                                                                             'Rs. 1000 as initial deposit.\nPlease '
                                                                             'Sign in with your new account to '
                                                                             'continue...',
                                                                        halign='center', valign='middle'))

            popup.size_hint = 0.6, 0.4
            popup.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            popup.open()

        t1.state = 'normal'
        t2.state = 'normal'
        t3.state = 'normal'
        self.manager.current = 'Welcome'
        self.manager.transition.direction = 'right'


class SignInInterface(Screen):
    def signin_btn(self, username: TextInput, password: TextInput):  # association

        with open('user_data.csv', 'r') as csvfile:
            sign_in = False
            csv_reader = reader(csvfile)
            for row in csv_reader:
                if row[3] == username.text and row[4] == password.text:
                    sign_in = True
            if not sign_in:
                l1 = Label(text='Please fill in all the entries correctly!', color='red', halign='center',
                           valign='middle')
                popup = Popup(title='Warning', content=l1, title_color='red', separator_color='red')
                popup.size_hint = 0.4, 0.2
                popup.open()

            else:
                UserInterface().receiveData(username.text)  # association
                self.manager.current = 'User Interface'


class UserInterface(Screen):

    @classmethod
    def receiveData(cls, username):
        cls.username = username

    def userInterface(self):
        with open('user_accounts.csv', 'r') as f:
            for row in reader(f):
                if row[0] == self.username:
                    accounts = eval(row[1])
                    break

        g = GridLayout()
        g.rows = 8
        g.padding = '100dp'
        g.spacing = '12dp'
        l1 = Label(text=f'\nWelcome, Dear {self.username}\n', font_size='30dp', bold=True, valign='middle',
                   halign='center')
        g.add_widget(l1)
        l2 = Label(text='Click on the account you would like to view:', font_size='18dp', valign='middle',
                   halign='center')
        g.add_widget(l2)

        class ComposedButton(Button):  # to display the concept of composition in OOP
            def __init__(self1, screen_name, **kwargs):
                super().__init__(**kwargs)
                self1.scr_name = screen_name

            def on_press(self1):
                self.manager.current = self1.scr_name
                if self1.scr_name == 'Sign In Interface':
                    self.manager.transition.direction = 'right'
                else:
                    self.manager.transition.direction = 'left'

                g.remove_widget(l1)
                g.remove_widget(l2)
                g.remove_widget(b5)

                try:  # to display exceptional handling
                    g.remove_widget(b1)  # in case these objects were not created
                except NameError:
                    pass
                try:
                    g.remove_widget(b2)
                except NameError:
                    pass
                try:
                    g.remove_widget(b3)
                except NameError:
                    pass
                try:
                    g.remove_widget(b4)
                except NameError:
                    pass

        # multiple if structure to allow the user to create as many accounts as required
        if not accounts:
            b1 = ComposedButton('Current Account Interface', text='Current Account')
            b1.background_color = 0.92, 0.747, 0.406, 0.58
            g.add_widget(b1)
            CurrentAccountInterface().receiveData(self.username)

        if 'Checking_Account' in accounts:
            b2 = ComposedButton('Checking Account Interface', text='Checking Account')
            b2.background_color = 0.89, 0.647, 0.306, 0.58
            g.add_widget(b2)
            CheckingAccountInterface().receiveData(self.username)

        if 'Savings_Account' in accounts:
            b3 = ComposedButton('Savings Account Interface', text='Savings Account')
            b3.background_color = 0.859, 0.549, 0.114, 0.58
            g.add_widget(b3)
            SavingsAccountInterface().receiveData(self.username)

        if 'Loan_Account' in accounts:
            b4 = ComposedButton('Loan Account Interface', text='Loan Account')
            b4.background_color = 0.561, 0.408, 0.196, 0.58
            g.add_widget(b4)
            LoanAccountInterface().receiveData(self.username)

        b5 = ComposedButton('Sign In Interface', text='Go Back', font_size='15dp', bold=True)
        b5.size_hint = None, None
        b5.size = '70dp', '35dp'
        g.add_widget(b5)
        self.add_widget(g)


class Account:  # this is the main parent class responsible to perform various account operations

    def deposit(self, account_name, user, overdraft=0):

        time_now = datetime.now().strftime("%H:%M:%S")
        date_now = datetime.now().strftime("%d-%m-%Y")
        popup = Popup(auto_dismiss=False, title='Amount Deposit')
        popup.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        popup.size_hint = (0.6, 0.4)

        bl = BoxLayout()
        bl.padding = '12dp'
        bl.orientation = 'vertical'

        label = Label(text='Enter the amount you would like to deposit:', halign='center', valign='middle')

        label.size_hint = 0.5, 0.5
        label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        bl.add_widget(label)

        t = IntInput(hint_text='Enter amount here...', multiline=False)
        t.size_hint = (0.5, 0.15)
        t.pos_hint = {'center_x': 0.5, 'top': 0.5}
        bl.add_widget(t)

        def end_deposit(instance):
            popup1 = Popup(title='Status',
                           content=Label(text=f'Rs.{t.text} successfully deposited to your account!'),
                           auto_dismiss=True)
            with open(f'{account_name}//{user}.csv', 'a+') as f:
                f.seek(0)
                final_line = f.readlines()[-1]
                balance = int(float(final_line.strip().split(',')[0]))
                overdraft1 = overdraft
                depositAmount = int(t.text)
                if account_name != 'CheckingAccounts':
                    writer(f).writerow([balance + depositAmount, depositAmount, 0, time_now, date_now])
                else:
                    if balance < 0:
                        overdraft1 = overdraft + depositAmount
                        if overdraft1 > 10000:
                            overdraft1 = 10000
                    writer(f).writerow(
                        [balance + depositAmount, depositAmount, 0, overdraft1, time_now, date_now])

            popup1.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            popup1.size_hint = (0.6, 0.2)
            popup1.open()
            popup.dismiss()

        t.bind(on_text_validate=end_deposit)
        popup.content = bl
        popup.open()

    def withdraw(self, account_name, user, overdraft=0):
        time_now = datetime.now().strftime("%H:%M:%S")
        date_now = datetime.now().strftime("%d-%m-%Y")

        popup = Popup(auto_dismiss=False, title='Amount Withdrawal')
        popup.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        popup.size_hint = (0.6, 0.4)

        bl = BoxLayout()
        bl.padding = '12dp'
        bl.orientation = 'vertical'
        content = f'\n(overdraft capacity is {overdraft})' if account_name == 'CheckingAccounts' else ''
        label = Label(text=f'Enter the amount you would like to withdraw{content}:', halign='center', valign='middle')

        label.size_hint = 0.6, 0.5
        label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        bl.add_widget(label)

        t = IntInput(hint_text='Enter amount here...', multiline=False)
        t.size_hint = (0.5, 0.15)
        t.pos_hint = {'center_x': 0.5, 'top': 0.5}
        bl.add_widget(t)

        def end_withdrawal(instance):
            with open(f'{account_name}//{user}.csv', 'a+') as f:
                f.seek(0)
                final_line = f.readlines()[-1].strip().split(',')
                balance = int(final_line[0])
                withdrawAmount = int(t.text)
                check = balance - withdrawAmount
                if check >= 0:
                    popup1 = Popup(title='Status',
                                   content=Label(text=f'Rs. {t.text} successfully withdrawn from your account!'),
                                   auto_dismiss=True)
                    if account_name == 'CheckingAccounts':
                        writer(f).writerow(
                            [check, 0, withdrawAmount, overdraft, time_now, date_now])
                    else:
                        writer(f).writerow([check, 0, withdrawAmount, time_now, date_now])

                else:
                    if account_name == 'CheckingAccounts':
                        store = False
                        if balance >= 0 > check >= -10000:  # for the first time when overdraft gets applied
                            # (initial balance was positive but after withdrawal, balance becomes negative)
                            overdraft1 = overdraft + check
                            store = True

                        elif balance < 0 and withdrawAmount <= overdraft:
                            # if the balance is already negative and more amount is getting withdrawn
                            overdraft1 = overdraft - withdrawAmount
                            store = True

                        if store:
                            popup1 = Popup(title='Status',
                                           content=Label(
                                               text=f'Rs. {t.text} successfully withdrawn from your account \nwith'
                                                    f' remaining overdraft capacity: Rs.{overdraft1}!'),
                                           auto_dismiss=True)
                            writer(f).writerow([check, 0, withdrawAmount, overdraft1, time_now, date_now])

                        else:   # if the withdrawn amount exceeds the credit limit
                            popup1 = Popup(title='Status', content=Label(text='Cannot withdraw more than overdraft '
                                                                              'limit!'), auto_dismiss=True)

                    else:  # if the withdrawn amount exceeds the credit limit
                        popup1 = Popup(title='Status', content=Label(text='Your balance is not sufficient for this '
                                                                          'withdrawal!'), auto_dismiss=True)

                popup1.pos_hint = {"center_x": 0.5, "center_y": 0.5}
                popup1.size_hint = (0.6, 0.25)
                popup1.open()
                popup.dismiss()

        t.bind(on_text_validate=end_withdrawal)
        popup.content = bl
        popup.open()

    def view_balance(self, account_name, user):

        with open(f'{account_name}//{user}.csv', 'a+') as f:
            f.seek(0)
            final_line = f.readlines()[-1].strip().split(',')
            balance = final_line[0]
        popup = Popup(title='Status', content=Label(text=f'Your current balance is Rs.{balance}!'))
        popup.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        popup.size_hint = (0.55, 0.2)
        popup.open()

    def viewReport(self, account_name, user, no_of_fields=5):

        popup = Popup(title='Transaction Report', auto_dismiss=False)
        sl = ScrollView()
        gl = GridLayout(cols=1)
        gl.padding = '35dp'
        gl.spacing = '10dp'
        if no_of_fields == 5:
            gl.cols = 5
        else:
            gl.cols = 6

        with open(f'{account_name}//{user}.csv', 'r') as f:
            data = []
            for row in reader(f):
                data.append(row)

        bl1 = BoxLayout(orientation='vertical')
        l1 = Label(text='BALANCE', bold=True)
        bl1.add_widget(l1)

        bl2 = BoxLayout(orientation='vertical')
        l2 = Label(text='DEPOSIT', bold=True)
        bl2.add_widget(l2)

        bl3 = BoxLayout(orientation='vertical')
        l3 = Label(text='WITHDRAWAL', bold=True)
        bl3.add_widget(l3)

        if no_of_fields == 6:
            bl4 = BoxLayout(orientation='vertical')
            l4 = Label(text='OVERDRAFT', bold=True)
            bl4.add_widget(l4)

        bl5 = BoxLayout(orientation='vertical')
        l5 = Label(text='TIME', bold=True)
        bl5.add_widget(l5)

        bl6 = BoxLayout(orientation='vertical')
        l6 = Label(text='DATE', bold=True)
        bl6.add_widget(l6)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        if no_of_fields == 5:
            widgets = [bl1, bl2, bl3, bl5, bl6]
            for i in range(len(data)):
                for j in range(5):
                    if j == (no_of_fields - 1) or j == (no_of_fields - 2):
                        l = Label(text=data[i][j])
                    else:
                        l = Label(text='Rs.' + data[i][j])
                    widgets[j].add_widget(l)
        else:
            widgets = [bl1, bl2, bl3, bl4, bl5, bl6]
            for i in range(len(data)):
                for j in range(6):
                    if j == (no_of_fields - 1) or j == (no_of_fields - 2):
                        l = Label(text=data[i][j])
                    else:
                        l = Label(text='Rs. ' + data[i][j])
                    widgets[j].add_widget(l)

        gl.add_widget(bl1)
        gl.add_widget(bl2)
        gl.add_widget(bl3)
        try:
            gl.add_widget(bl4)
        except NameError:
            pass
        gl.add_widget(bl5)
        gl.add_widget(bl6)

        button.bind(on_press=popup.dismiss)
        fl = FloatLayout()
        fl.size_hint = 0.1, 0.1
        fl.add_widget(button)

        gl.add_widget(fl)
        sl.add_widget(gl)
        popup.add_widget(sl)
        popup.open()

    def __eq__(self, other):  # operator overloading
        return isinstance(self, Account) == isinstance(other, Account)


class CurrentAccountInterface(Screen, Account):
    @classmethod
    def receiveData(cls, username):
        cls.username = username

    def deposit(self):  # method overriding
        super().deposit('BasicAccounts', self.username)

    def withdraw(self):
        super().withdraw('BasicAccounts', self.username)

    def view_balance(self):
        super().view_balance('BasicAccounts', self.username)

    def viewReport(self):
        super().viewReport('BasicAccounts', self.username)


class CheckingAccountInterface(Screen, Account):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.credit_limit = 10000

    @classmethod
    def receiveData(cls, username):
        cls.username = username

    def deposit(self):
        super().deposit('CheckingAccounts', self.username, self.get_overdraft())

    def withdraw(self):
        super().withdraw('CheckingAccounts', self.username, self.get_overdraft())

    def view_balance(self):
        super().view_balance('CheckingAccounts', self.username)

    def viewReport(self):
        super().viewReport('CheckingAccounts', self.username, 6)

    def get_overdraft(self):
        with open(f'CheckingAccounts//{self.username}.csv') as f:
            f.seek(0)
            final_line = f.readlines()[-1].strip().split(',')
            overdraft = int(final_line[3])
            return overdraft


class SavingsAccountInterface(Screen, Account):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.interest_rate = 0.03

    @classmethod
    def receiveData(cls, username):
        cls.username = username

    def deposit(self):
        super().deposit('SavingAccounts', self.username)

    def withdraw(self):
        super().withdraw('SavingAccounts', self.username)

    def view_balance(self):
        super().view_balance('SavingAccounts', self.username)

    def viewReport(self):
        super().viewReport('SavingAccounts', self.username)

    def add_interest(self):
        with open(f'SavingAccounts//{self.username}.csv', 'a+') as f:
            f.seek(0)
            checks = []
            for row in reader(f):
                if 'credit' in row[4]:
                    checks.append(row)

            if checks:
                f.seek(0)
                final_line = f.readlines()[-1].strip().split(',')
                balance = final_line[0]
                last_credit_date = checks[-1][4][:10].split('-')
                last_credit_date = date(int(last_credit_date[2]), int(last_credit_date[1]), int(last_credit_date[0]))
                days_passed = (date.today() - last_credit_date).days
                if days_passed >= 30:
                    time_now = datetime.now().strftime("%H:%M:%S")
                    date_now = datetime.now().strftime("%d-%m-%Y")
                    interest = (float(balance) * self.interest_rate) * (days_passed // 30)
                    balance = float(balance) + interest
                    writer(f).writerow([int(balance), int(interest), 0, time_now, date_now + ' credit'])


class LoanAccountInterface(Screen, Account):

    @classmethod
    def receiveData(cls, username):
        cls.username = username

    def loan_acquisition(self, user):
        popup = Popup(auto_dismiss=False, title='Loan Acquisition')
        popup.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        popup.size_hint = (0.9, 0.7)

        bl = BoxLayout()
        bl.padding = '12dp'
        bl.orientation = 'vertical'

        def loan_save(instance):
            loan_term = int(t3.text)
            principal_amount = int(t2.text)
            if not 0 < loan_term < 120:
                loan_term = 120
            with open(f'LoanAccounts//{user}.csv', 'a+') as f:
                f.seek(0)
                loan_pay = int(principal_amount * (0.03 + (1 / loan_term)))
                writer(f).writerow([principal_amount, date.today(), 0, loan_term, loan_pay, t1.text])
                # principal amount, date of taking loan, current month number, loan duration(in months),
                # loan pay, asset

            popup1 = Popup(title='Status',
                           content=Label(
                               text=f'Rs. {str(principal_amount)} as loan successfully deposited to your account!\n'
                                    f'Duration: {str(loan_term)} months', halign='center',
                               valign='middle'), auto_dismiss=True)
            popup1.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            popup1.size_hint = (0.6, 0.2)
            popup1.open()

        def enable_input(instance):
            if t1.text:
                asset = t1.text
                label2.disabled = False
                label3.disabled = False
                t2.disabled = False
                t3.disabled = False

        label1 = Label(text='Our secured loan account policy requires the collateral for mortgage as your asset.\n'
                            'Please enter the property address you plan to offer as a securing asset:',
                       halign='center', valign='middle')
        bl.add_widget(label1)

        t1 = TextInput(hint_text='Enter address here...', multiline=False)
        t1.size_hint = (0.6, 0.4)
        t1.pos_hint = {'center_x': 0.5, 'top': 0.5}
        t1.bind(on_text_validate=enable_input)
        bl.add_widget(t1)

        label2 = Label(text='Enter the amount you would like to loan from the bank(monthly interest rate = 3%):',
                       halign='center', valign='middle', disabled=True)
        bl.add_widget(label2)

        t2 = IntInput(hint_text='Enter amount here...', multiline=False, disabled=True)
        t2.size_hint = (0.4, 0.4)
        t2.pos_hint = {'center_x': 0.5, 'top': 0.5}
        bl.add_widget(t2)

        label3 = Label(text='Enter loan duration in months(not more than 120 months):', halign='center',
                       valign='middle', disabled=True)
        bl.add_widget(label3)

        t3 = IntInput(hint_text='Enter duration here...', multiline=False, disabled=True)
        t3.size_hint = (0.4, 0.4)
        t3.pos_hint = {'center_x': 0.5, 'top': 0.5}
        t3.bind(on_text_validate=popup.dismiss)
        bl.add_widget(t3)

        popup.bind(on_dismiss=loan_save)
        popup.content = bl
        popup.open()

    def loan_payment(self):

        data = self.getData(self.username)
        principal_amount = int(data[0])
        last_pay_date = data[1].split('-')
        last_pay_date = date(int(last_pay_date[0]), int(last_pay_date[1]), int(last_pay_date[2]))
        days_passed = (date.today() - last_pay_date).days
        current_month = int(data[2]) + 1
        loan_term = int(data[3].strip())
        loan_pay = int(data[4])
        asset = data[5].strip()

        if current_month >= loan_term:
            content = 'Congratulations!\nYou have successfully completed you loan payments.'

        elif days_passed // 30 == 1:
            content = f'Rs.{loan_pay} successfully deposited for month {current_month}'
            with open(f'LoanAccounts//{self.username}.csv', 'a+') as f:
                f.seek(0)
                writer(f).writerow([principal_amount, date.today(), current_month, loan_term,
                                    loan_pay, asset])

        elif days_passed // 30 == 0:
            content = 'You have already payed for this month.'

        else:
            content = 'Unfortunately, you did not pay for more than two months in a row.\nYour account has now ' \
                      'been frozen temporarily.\nPlease contact a franchise to unfreeze your account!'

        popup = Popup(title='Status', content=Label(text=content, halign='center', valign='middle'))
        popup.size_hint = 0.6, 0.3
        popup.open()

    def viewReport(self, user=''):
        if user == '':
            user = self.username
        popup = Popup(title='Transaction Report', auto_dismiss=False)
        sl = ScrollView()
        gl = GridLayout()
        gl.cols = 6
        with open(f'LoanAccounts//{user}.csv', 'r') as f:
            data = []
            for row in reader(f):
                data.append(row)

        bl1 = BoxLayout(orientation='vertical')
        l1 = Label(text='PRINCIPAL', bold=True)
        bl1.add_widget(l1)

        bl2 = BoxLayout(orientation='vertical')
        l2 = Label(text='PAY DATE', bold=True)
        bl2.add_widget(l2)

        bl3 = BoxLayout(orientation='vertical')
        l3 = Label(text='CURR. MONTH', bold=True)
        bl3.add_widget(l3)

        bl4 = BoxLayout(orientation='vertical')
        l4 = Label(text='DURATION', bold=True)
        bl4.add_widget(l4)

        bl5 = BoxLayout(orientation='vertical')
        l5 = Label(text='LOAN PAY', bold=True)
        bl5.add_widget(l5)

        bl6 = BoxLayout(orientation='vertical')
        l6 = Label(text='ASSET ADDRESS', bold=True)
        bl6.add_widget(l6)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        widgets = [bl1, bl2, bl3, bl4, bl5, bl6]
        for i in range(len(data)):
            for j in range(6):

                if j == 0 or j == 4:
                    label = Label(text='Rs. ' + str(data[i][j]))
                elif j == 3:
                    label = Label(text=str(data[i][j]) + ' month(s)')
                else:
                    label = Label(text=data[i][j])

                widgets[j].add_widget(label)

        gl.add_widget(bl1)
        gl.add_widget(bl2)
        gl.add_widget(bl3)
        gl.add_widget(bl4)
        gl.add_widget(bl5)
        gl.add_widget(bl6)

        button.bind(on_press=popup.dismiss)
        fl = FloatLayout()
        fl.size_hint = 0.1, 0.1
        fl.add_widget(button)

        gl.add_widget(fl)
        sl.add_widget(gl)
        popup.add_widget(sl)
        popup.open()

    @staticmethod
    def getData(user):
        with open(f'LoanAccounts//{user}.csv', 'a+') as f:
            f.seek(0)
            data = f.readlines()[-1].split(',')
            return data

    def viewTC(self):
        content = '1. Loan will not be granted for more then 120 months(10 years).\n' \
                  '2. 3% interest rate per month will be applied to the granted loan.\n' \
                  '3. Monthly loan payment must be made certain.\n' \
                  '4. The bank has the right to summon the asset in case of non-compliance.'
        popup = Popup(title='Status', content=Label(text=content))
        popup.size_hint = 0.65, 0.4
        popup.open()

    def loan_details(self):
        data = self.getData(self.username)
        content = f'Principal Amount = Rs. {data[0]}\n' \
                  f'Interest Rate = 3%\n' \
                  f'Current month = {data[2]}\n' \
                  f'Loan Term = {data[3]}\n' \
                  f'Monthly Loan Payment= Rs. {data[4]}\n' \
                  f'Collateral Asset Address = {data[5]}'

        popup = Popup(title='Status', content=Label(text=content))
        popup.size_hint = 0.5, 0.5
        popup.open()


class AdminVerification(Screen):
    __user_name = ['Mahwish', 'Tooba', 'Aqiba']
    __pwd = 'abc'

    def admin_btn(self, username: TextInput, password: TextInput):
        if username.text in self.__user_name and password.text == self.__pwd:
            self.manager.current = 'Admin Portal'

        else:
            l1 = Label(text='Please fill in all the entries correctly!', color='red', halign='center',
                       valign='middle')
            popup = Popup(title='Warning', content=l1, title_color='red', separator_color='red')
            popup.size_hint = 0.4, 0.2
            popup.open()


class UserDataSheet(Screen):
    def display(self):
        sl = ScrollView()

        gl = GridLayout(cols=1, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        gl.padding = '35dp'
        gl.spacing = '10dp'

        l = Label(text='MTABank Users', font_size='30sp', bold=True, valign='middle', halign='center',
                  size_hint_y=None)
        l.pos_hint = {'left': 1}
        gl.add_widget(l)

        label = Label(text='Select the user datasheet you would like to view:', size_hint_y=None)
        gl.add_widget(label)

        with open('user_data.csv') as f:
            entries = []
            f.seek(0)
            for row in reader(f):
                entries.append(row[3].strip())

            def report(instance, i_):
                with open('user_data.csv') as f:
                    f.seek(0)
                    for row in reader(f):
                        if i_ in row:
                            data = row
                            break

                content = f'{"First Name:": <14}{data[0]}\n' \
                          f'{"Last Name:": <14}{data[1]}\n' \
                          f'{"Address:": <14}{data[2]}\n' \
                          f'{"Username:": <14}{data[3]}\n' \
                          f'{"Password:": <14}{data[4]}\n'

                popup = Popup(title='User Report', content=Label(text=content))
                popup.size_hint = 0.5, 0.5
                popup.open()

            for i in range(len(entries)):
                b = Button(text=entries[i], size_hint_y=None, background_color=(0, 0.812, 0.925, 0.6))
                b.bind(on_press=lambda dt, i_=i: report(dt, entries[i_]))
                gl.add_widget(b)

            button = Button(text='Go Back', font_size='15dp', bold=True)
            button.size_hint = None, None
            button.size = '70dp', '35dp'

            def switch_screen(instance):
                self.manager.current = 'Admin Portal'
                self.manager.transition.direction = 'right'
                gl.clear_widgets()

        button.bind(on_press=switch_screen)
        gl.add_widget(button)

        sl.add_widget(gl)
        self.add_widget(sl)


class BasicAccountReport(Screen):
    def display(self):
        sl = ScrollView()

        gl = GridLayout(cols=1, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        gl.padding = '35dp'
        gl.spacing = '10dp'

        entries = listdir('BasicAccounts//')
        entries = [i[:-4] for i in entries]

        l = Label(text='Current Account Users', font_size='30sp', bold=True, valign='middle', halign='center',
                  size_hint_y=None)
        l.pos_hint = {'left': 1}
        gl.add_widget(l)

        label = Label(text='Select the user account you would like to view:', size_hint_y=None)
        gl.add_widget(label)

        report = lambda dt, entry_num: Account.viewReport(self, 'BasicAccounts', entries[entry_num])

        for i in range(len(entries)):
            b = Button(text=entries[i], size_hint_y=None, background_color=(0, 0.812, 0.925, 0.6))
            b.bind(on_press=lambda dt, i_=i: report(dt, i_))
            gl.add_widget(b)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        def switch_screen(instance):
            self.manager.current = 'Admin Portal'
            self.manager.transition.direction = 'right'
            gl.clear_widgets()

        button.bind(on_press=switch_screen)
        gl.add_widget(button)

        sl.add_widget(gl)
        self.add_widget(sl)


class CheckingAccountReport(Screen):
    def display(self):
        sl = ScrollView()

        gl = GridLayout(cols=1, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        gl.padding = '35dp'
        gl.spacing = '10dp'

        entries = listdir('CheckingAccounts//')
        entries = [i[:-4] for i in entries]

        l = Label(text='Checking Account Users', font_size='30sp', bold=True, valign='middle', halign='center',
                  size_hint_y=None)
        l.pos_hint = {'left': 1}
        gl.add_widget(l)

        label = Label(text='Select the user account you would like to view:', size_hint_y=None)
        gl.add_widget(label)

        report = lambda dt, entry_num: Account.viewReport(self, 'CheckingAccounts', entries[entry_num])

        for i in range(len(entries)):
            b = Button(text=entries[i], size_hint_y=None, background_color=(0, 0.812, 0.925, 0.6))
            b.bind(on_press=lambda dt, i_=i: report(dt, i_))
            gl.add_widget(b)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        def switch_screen(instance):
            self.manager.current = 'Admin Portal'
            self.manager.transition.direction = 'right'
            gl.clear_widgets()

        button.bind(on_press=switch_screen)
        gl.add_widget(button)

        sl.add_widget(gl)
        self.add_widget(sl)


class SavingAccountReport(Screen):
    def display(self):
        sl = ScrollView()

        gl = GridLayout(cols=1, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        gl.padding = '35dp'
        gl.spacing = '10dp'

        entries = listdir('SavingAccounts//')
        entries = [i[:-4] for i in entries]

        l = Label(text='Saving Account Users', font_size='30sp', bold=True, valign='middle', halign='center',
                  size_hint_y=None)
        l.pos_hint = {'left': 1}
        gl.add_widget(l)

        label = Label(text='Select the user account you would like to view:', size_hint_y=None)
        gl.add_widget(label)

        report = lambda dt, entry_num: Account.viewReport(self, 'SavingAccounts', entries[entry_num])

        for i in range(len(entries)):
            b = Button(text=entries[i], size_hint_y=None, background_color=(0, 0.812, 0.925, 0.6))
            b.bind(on_press=lambda dt, i_=i: report(dt, i_))
            gl.add_widget(b)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        def switch_screen(instance):
            self.manager.current = 'Admin Portal'
            self.manager.transition.direction = 'right'
            gl.clear_widgets()

        button.bind(on_press=switch_screen)
        gl.add_widget(button)

        sl.add_widget(gl)
        self.add_widget(sl)


class LoanAccountReport(Screen):
    def display(self):
        sl = ScrollView()

        gl = GridLayout(cols=1, size_hint_y=None)
        gl.bind(minimum_height=gl.setter('height'))
        gl.padding = '35dp'
        gl.spacing = '10dp'

        entries = listdir('LoanAccounts//')
        entries = [i[:-4] for i in entries]

        l = Label(text='Loan Account Users', font_size='30sp', bold=True, valign='middle', halign='center',
                  size_hint_y=None)
        l.pos_hint = {'left': 1}
        gl.add_widget(l)

        label = Label(text='Select the user account you would like to view:', size_hint_y=None)
        gl.add_widget(label)

        report = lambda dt, entry_num: LoanAccountInterface.viewReport(self, entries[entry_num])
        for i in range(len(entries)):
            b = Button(text=entries[i], size_hint_y=None, background_color=(0, 0.812, 0.925, 0.6))
            b.bind(on_press=(lambda dt, i_=i: report(dt, i_)))
            gl.add_widget(b)

        button = Button(text='Go Back', font_size='15dp', bold=True)
        button.size_hint = None, None
        button.size = '70dp', '35dp'

        def switch_screen(instance):
            self.manager.current = 'Admin Portal'
            self.manager.transition.direction = 'right'
            gl.clear_widgets()

        button.bind(on_press=switch_screen)
        gl.add_widget(button)

        sl.add_widget(gl)
        self.add_widget(sl)


class LinkLabel(ButtonBehavior, Label):
    pass


class IntInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit():
            return super().insert_text(substring, from_undo=from_undo)


class MTABank(App):  # name of this App class should be the same as your kivy file's name
    pass



app = MTABank().run()
