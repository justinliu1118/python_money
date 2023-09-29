import sys
import os

class colors:
    '''set output string colors'''
    GREEN = '\033[92m' # green
    YELLOW = '\033[93m' # yellow
    RED = '\033[91m' # red
    RESET = '\033[0m' # reset

class Record:
    '''store a record'''
    def __init__(self, category, item, amount):
        '''initialize Record object'''
        self._category = category
        self._item = item
        self._amount = int(amount)

    def get_category(self):
        '''getter methods to get category'''
        return self._category
    def get_item(self):
        '''getter methods to get item'''
        return self._item
    def get_amount(self):
        '''getter methods to get amount'''
        return self._amount
    category = property(lambda self: self.get_category()) # decorator
    item = property(lambda self: self.get_item())
    amount = property(lambda self: self.get_amount())


class Records:
    '''store a list of records'''
    def __init__(self):
        '''initialize Records object'''
        self._records = []
        self._money = 0
        try:
            fh = open('records.txt', 'r')
            if os.path.getsize('records.txt') == 0: # Error1: empty file
                print(f'{colors.YELLOW}The input file is empty!{colors.RESET}')
                raise OSError
            try:
                self._money = int(fh.readline().rstrip('\n'))
            except: # Error2: money cannot convert to int
                raise ValueError(f'{colors.RED}Cannot convert the anount of money to int.\n{colors.RESET}')
            tmpfile = fh.readlines()
            try:
                for strings in tmpfile:
                    strings.rstrip('\n')
                    s1, s2, s3= strings.split(', ') # split by space
                    self._records.append(Record(s1, s2, int(s3))) # append to record list
            except: # Error3: input file cannot be interpreted as record
                raise ValueError(f'{colors.RED}The input file cannot be interpreted as record.\n{colors.RESET}')
            fh.close()
            print(f'{colors.GREEN}Welcome back!{colors.RESET}')
        except OSError:
            try:
                self._money = int(input('How much money do you have? '))
            except ValueError: # Error 4: cannot convert money to integer
                self._money = 0
                sys.stderr.write(f'{colors.RED}Invalid value for money. Set to 0 by defult.\n{colors.RESET}')
        except ValueError as err:
            sys.stderr.write(str(err))
            try:
                self._money = int(input('How much money do you have? '))
            except ValueError:
                self._money = 0
                sys.stderr.write(f'{colors.RED}Invalid value for money. Set to 0 by defult.\n{colors.RESET}')
    
    
    def add(self, record, categories):
        '''input multiple record '''
        try:
            for i in record:
                try:
                    new_rec= Record(*(i.split(' '))) # split by space
                except: # Error 5: cannot split into two strings
                    raise ValueError(f"{colors.RED}Failed to add '{i}' to record. Cannot split to three strings.\n{colors.RESET}")
                if not categories.is_category_valid(new_rec.category, categories.categories):
                    raise ValueError(f"{colors.RED}'{new_rec.category}' is not a valid category.\n{colors.RESET}")
                try:
                    self._money += new_rec.amount
                    self._records.append(new_rec) # append to record list
                except: # Error 6: cannot convert the secord string to int
                    raise ValueError(f"{colors.RED}Cannot convert the third string '{new_rec.amount}' to int.\n{colors.RESET}")
        except ValueError as err:
            sys.stderr.write(str(err))
    
    
    def view(self):
        ''' View the records and the balance '''
        print("Here's your expense and income records:")
        print(f"{'Category':<21s}{'Description':<21s}Amount\n" + '='*20 + ' ' + '='*20 + ' ' +'='*6)
        for item in self._records:
            try:
                if int(item.amount) >= 0:
                    print(f"{item.category:<21s}{item.item:<21s}{colors.GREEN}{item.amount:<6d}{colors.RESET}")
                else:
                    print(f"{item.category:<21s}{item.item:<21s}{colors.RED}{item.amount:<6d}{colors.RESET}")
            except ValueError as err:
                print('%s' % str(err))
        print('='*20 + ' ' + '='*20 + ' ' +'='*6)
        if self._money >= 0:
            print(f"Now you have {colors.GREEN}{self._money}{colors.RESET} dollars!")
        else:
            print(f"Now you have {colors.RED}{self._money}{colors.RESET} dollars!")
    
    def delete(self):
        ''' Delete a record '''
        print("Record List:")
        if(len(self._records)):
            for item in self._records:
                if item.amount >= 0:
                    print(f"{self._records.index(item)}: {item.category:<21}{item.item:<21}{colors.GREEN}{item.amount:<6d}{colors.RESET}")
                else:
                    print(f"{self._records.index(item)}: {item.category:<21}{item.item:<21}{colors.RED}{item.amount:<6d}{colors.RESET}")
            try:
                deleteidx = int(input("Select the index of the item you want to delete: "))
                self._money -= self._records[deleteidx].amount
                self._records.remove(self._records[deleteidx])
            except ValueError: # Error 7: input cannot convert to int
                sys.stderr.write(f'{colors.RED}Invalid format. Fail to delete a record.\n{colors.RESET}')
            except IndexError: # Error 8: index out of range
                sys.stderr.write(f"{colors.RED}There's no record with index '{deleteidx}'. Fail to delete a record.\n{colors.RESET}")
        else:
            print(f"{colors.YELLOW}The record list is empty, nothing to delete!{colors.RESET}")
    
    def find(self, target, subcategories):
        ''' find and print the subcategories'''
        total = 0
        subrecords = filter(lambda v: v.category in subcategories, self._records)
        print(f"Here's your expense and income records under category '{target}':")
        print(f"{'Category':<21s}{'Description':<21s}Amount\n" + '='*20 + ' ' + '='*20 + ' ' +'='*6)
        for item in subrecords:
            if item.amount >= 0:
                print(f"{item.category:<21s}{item.item:<21s}{colors.GREEN}{item.amount:<6d}{colors.RESET}")
            else:
                print(f"{item.category:<21s}{item.item:<21s}{colors.RED}{item.amount:<6d}{colors.RESET}")
            total += item.amount
        print('='*20 + ' ' + '='*20 + ' ' +'='*6)
        if self._money >= 0:
            print(f"The total amount above is {colors.GREEN}{total}{colors.RESET}.")
        else:
            print(f"The total amount above is {colors.RED}{total}{colors.RESET}.")

    
    def save(self):
        ''' create record file before stopping the program'''
        with open('records.txt', 'w') as fh:
            fh.write(str(self._money) + '\n')
            output = [f'{v.category}, {v.item}, {v.amount}' + '\n' for v in self._records]
            fh.writelines(output)
        print(f'{colors.GREEN}Bye!{colors.RESET}')  


class Categories:
    '''categories of the records'''
    def __init__(self):
        '''initialize Categories object'''
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self, L, tab=0):
        '''A recursive function to view categories'''
        if type(L) in {list, tuple}:
            for v in L:
                self.view(v, tab+1) # iterate with parameter tab+1
        else:
            s = ' ' * 4 * (tab-1) # print space
            s += '- ' + L # print category
            print(s)

    
    
    
    def is_category_valid(self, category, categories):
        ''' A recursive function to test if the input category is valid'''
        result = False
        for i in categories:
            if type(i) != list:
                if i == category:
                    return True
            else:
                return self.is_category_valid(category, i)
        return result
    
    def find_subcategories(self, category):
        '''find subcategories using recursive generator'''
        def find_subcategories_gen(category, categories, found=False):
            '''A recursive generator to yield the subcategories of the target category'''
            if type(categories) == list:
                for index, child in enumerate(categories):
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        found = True # found the category, then found = True to yield the subcategories
                    yield from find_subcategories_gen(category, child, found)
            else:
                if categories == category or found:
                    yield categories
        # list comprehension to flatten the nested list
        return [i for i in find_subcategories_gen(category, self._categories)]
    
    
    #def flatten(self, L):
    #    ''' A recursive function to flatten a nested list'''
    #    if type(L) == list:
    #        result = []
    #        for child in L:
    #            result.extend(self.flatten(child))
    #        return result
    #    else:
    #        return [L]

    #def find_subcategories(self, category, categories):
    #    ''' A recursive function to find subcategories'''
    #   if type(categories) == list:
    #       for v in categories:
    #           p = self.find_subcategories(category, v)
    #           if p == True:
    #               if found, return the flatten list including itself
    #               and its subcategories
    #               index = categories.index(v)
    #               if index + 1 < len(categories) and type(categories[index + 1]) == list: # there is subcategories
    #                   return self.flatten(categories[index:index + 2])
    #               else: # no subcategories
    #                  return [v]
    #           if p != []:
    #               return p
    #   return True if categories == category else [] # return [] instead of False if not found

    def get_categories(self):
        '''getter method to get categories'''
        return self._categories
    categories = property(lambda self: self.get_categories())

# main
try:
    categories = Categories()
    records = Records()
    while True:
        command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
        if command == 'add':
            record = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n').split(', ')
            records.add(record, categories)
        elif command == 'view':
            records.view()
        elif command == 'delete':
            records.delete()
        elif command == 'view categories':
            categories.view(categories.categories)
        elif command == 'find':
            category = input('Which category do you want to find? ')
            target_categories = categories.find_subcategories(category)
            records.find(category, target_categories)
        elif command == 'exit':
            break
        else:
            raise ValueError
except ValueError: # Error 9: the command is not add/view/delete/exit
    sys.stderr.write(f'{colors.RED}Invalid command. Try again!\n{colors.RESET}')
except KeyboardInterrupt: # Error10: manually stop the program
    sys.stderr.write(f'{colors.YELLOW}Manually stop the program\n{colors.RESET}')
finally:
    records.save()