#!/usr/bin/python3
""" Console Module"""

import os
import re
import cmd
import uuid
import shlex
import models
from datetime import datetime
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
    __classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    def precmd(self, line):
        return super().precmd(line)

    def do_create(self, args):
        """ Create an object of any class
        usage: create <class name> <param 1> <param 2> ...
        param = <key name>=<value>
        """
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}
        if class_match is not None:
            class_name = class_match.group('name')
            params_str = args[len(class_name):].strip()
            params = params_str.split(' ')
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'
            param_pattern = '{}=({}|{}|{})'.format(
                name_pattern,
                str_pattern,
                float_pattern,
                int_pattern
            )
            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v is not None:
                        obj_kwargs[key_name] = float(float_v)
                    if int_v is not None:
                        obj_kwargs[key_name] = int(int_v)
                    if str_v is not None:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            class_name = args
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if not hasattr(obj_kwargs, 'id'):
                obj_kwargs['id'] = str(uuid.uuid4())
            if not hasattr(obj_kwargs, 'created_at'):
                obj_kwargs['created_at'] = str(datetime.now())
            if not hasattr(obj_kwargs, 'updated_at'):
                obj_kwargs['updated_at'] = str(datetime.now())
            new_instance = HBNBCommand.__classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.__classes[class_name]()
            for key, value in obj_kwargs.items():
                if key not in ignored_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

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
