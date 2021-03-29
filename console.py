#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*setterss> or <**kwsetterss>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _setterss = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain settersuments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition setterss: (<id>, [<delim>], [<*setterss>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if settersuments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *setterss or **kwsetterss
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _setterss = pline
                    else:
                        _setterss = pline.replace(',', '')
                        # _setterss = _setterss.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _setterss])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, setters):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, setterss):
        """ Create an object of any class"""
        if not setterss:
            print("** class name missing **")
            return

        console_commands = setterss.split(' ')

        if console_commands[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        new_obj = HBNBCommand.classes[console_commands[0]]()

        for i in range(1, len(console_commands)):

            setters = console_commands[i].split('=', 1)
            value = ""

            if setters[1][0] == '"' or setters[1][0] == "'":
                value = setters[1][1:-1]
                if '"' or "'" in value:
                    value = value.replace('"', '\"')
                if "_" in value:
                    value = value.replace('_', ' ')
            else:
                if '.' in setters[1]:
                    try:
                        value = float(setters[1])
                    except:
                        continue
                else:
                    try:
                        value = int(setters[1])
                    except:
                        continue
            if value != "":
                setattr(new_obj, setters[0], value)
  
        storage.save()
        print(new_obj.id)
        storage.save()


    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, setterss):
        """ Method to show an individual object """
        new = setterss.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing setterss
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, setterss):
        """ Destroys a specified object """
        new = setterss.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, setterss):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if setterss:
            setterss = setterss.split(' ')[0]  # remove possible trailing setterss
            if setterss not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == setterss:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, setterss):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if setterss == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, setterss):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwsetterss = ''

        # isolate cls from id/setterss, ex: (<cls>, delim, <id/setterss>)
        setterss = setterss.partition(" ")
        if setterss[0]:
            c_name = setterss[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from setterss
        setterss = setterss[2].partition(" ")
        if setterss[0]:
            c_id = setterss[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwsetterss or setterss
        if '{' in setterss[2] and '}' in setterss[2] and type(eval(setterss[2])) is dict:
            kwsetterss = eval(setterss[2])
            setterss = []  # reformat kwsetterss into list, ex: [<name>, <value>, ...]
            for k, v in kwsetterss.items():
                setterss.append(k)
                setterss.append(v)
        else:  # isolate setterss
            setterss = setterss[2]
            if setterss and setterss[0] == '\"':  # check for quoted setters
                second_quote = setterss.find('\"', 1)
                att_name = setterss[1:second_quote]
                setterss = setterss[second_quote + 1:]

            setterss = setterss.partition(' ')

            # if att_name was not quoted setters
            if not att_name and setterss[0] != ' ':
                att_name = setterss[0]
            # check for quoted val setters
            if setterss[2] and setterss[2][0] == '\"':
                att_val = setterss[2][1:setterss[2].find('\"', 1)]

            # if att_val was not quoted setters
            if not att_val and setterss[2]:
                att_val = setterss[2].partition(' ')[0]

            setterss = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(setterss):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = setterss[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
