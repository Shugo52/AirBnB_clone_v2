#!/usr/bin/python3
""" Console Module"""

import re
import cmd
import shlex
import models
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ Defines the 'HBNBCommand' class
    This class inherits from 'cmd.Cmd

    Attributes:
        prompt: prompt string
        __classes: list of all classes
    """
    prompt = "(hbnb) "
    __classes = [
        "BaseModel",
        "User",
        "Place",
        "City",
        "Review",
        "Amenity",
        "State"
    ]

    def precmd(self, line):
        return super().precmd(line)

    def do_create(self, args):
        """ Usage: create <class name> <param 1> <param 2>...
        where param -> key=value
        Creates a new class instance and prints its id
        """
        # split args
        arg = args.split(' ')

        # param value syntax pattern
        str_patttern = r'^"([^"]|\")*"$'
        float_pattern = r'([\d]+\.[\d]+)'
        int_pattern = r'^\d+$'

        # validate input
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            # check if parameters passed
            if len(arg) > 1:
                # argument container(dictionary)
                kwargs = {}

                for i in range(len(arg)):
                    if '=' in arg[i]:
                        kw = re.split(r'=', arg[i])

                        # Check for value syntax match
                        match_str = re.search(str_patttern, kw[1])
                        match_float = re.search(float_pattern, kw[1])
                        match_int = re.search(int_pattern, kw[1])

                        # Update values if any match
                        if match_str:
                            tmp = shlex.split(arg[i])
                            kw = tmp[0].split('=')
                            kw[1] = re.sub(r'_', ' ', kw[1])
                        if match_float:
                            kw[1] = float(kw[1])
                        if match_int:
                            kw[1] = int(kw[1])

                        # add to container
                        kwargs[kw[0]] = kw[1]

                # create instance and save to storage
                print(eval(arg[0])(**kwargs).id)
            else:
                print(eval(arg[0])().id)
            models.storage.save()

    def do_show(self, args):
        """Usage: show <class> <id>
        Prints string representation of instance of class
        based on id"""
        arg = shlex.split(args)
        all_objs = models.storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif f"{arg[0]}.{arg[1]}" not in all_objs.keys():
            print("** no instance found **")
        else:
            print(all_objs[f"{arg[0]}.{arg[1]}"])

    def do_destroy(self, args):
        """Usage: destroy <class> <id>
        Delete a class instance based on id
        """
        arg = shlex.split(args)
        all_objs = models.storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif f"{arg[0]}.{arg[1]}" not in all_objs.keys():
            print("** no instance found **")
        else:
            del all_objs[f"{arg[0]}.{arg[1]}"]
            models.storage.save()

    def do_all(self, args):
        """Usage: all <class>  or  all
        Prints string representation of all instances of available"""
        arg = shlex.split(args)
        all_objs = models.storage.all()
        if len(arg) == 0:
            for obj_id in all_objs.keys():
                obj = all_objs[obj_id]
                print(obj)
        elif arg[0] and arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            for key in all_objs.keys():
                if arg[0] in key:
                    print(all_objs[key])

    def do_update(self, args):
        """Usage:
        update <class name> <id> <attribute name> '<attribute value>'
        Updates an instance based on class id by adding or updating
        attributes"""
        arg = shlex.split(args)[0:4]
        all_objs = models.storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif f"{arg[0]}.{arg[1]}" not in all_objs.keys():
            print("** no instance found **")
        elif len(arg) == 2:
            print("** attribute name missing **")
        elif len(arg) == 3:
            print("** value missing **")
        else:
            updateDict = all_objs[f"{arg[0]}.{arg[1]}"]
            updateDict.__dict__[arg[2]] = arg[3]
            updateDict.save()

    def do_quit(self, line):
        """ Quit command to exit the program
        """
        return True

    def emptyline(self):
        pass

    def do_EOF(self, line):
        """ End of line method"""
        print('')
        return True

    def default(self, line):
        """ Called when cmd prefix is not recognized"""
        if '.' not in line:
            super().default(line)
            return

        model = line.split('.')

        if model[1] == "all()":
            self.do_all(model[0])
            return

        if model[1] == "count()":
            count = 0
            for key in models.storage.all().keys():
                if model[0] in key:
                    count += 1
            print(count)
            return

        if "show" in model[1]:
            id = model[1][5:-1]
            self.do_show(f"{model[0]} {id}")
            return

        if "destroy" in model[1]:
            id = model[1][8:-1]
            self.do_destroy(f"{model[0]} {id}")
            return

        if "update" in model[1]:
            if model[1] == "update()":
                self.do_update(model[0])
                return

            args = eval(model[1][7:-1])

            if "update" in model[1]:
                args = line.split(".")
                if args[1] == "update()":
                    self.do_update(model[0])
                    return
                u_args = eval(args[1][7:-1])

                if isinstance(u_args[1], dict):
                    id, attr = u_args
                    for key, value in attr.items():
                        self.do_update(f"{model[0]} {id} {key} {value}")
                    return

                if type(u_args) != str:
                    u_args = " ".join(u_args)

                self.do_update(f"{model[0]} {u_args}")
                return

        super().default(line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
