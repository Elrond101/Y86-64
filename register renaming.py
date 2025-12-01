from basic import *
def renaming(reg_num, modify_content, reg_renaming): #reg_renaming = [empty_names, value_key]
    empty_names = reg_renaming[0]
    value_key = reg_renaming[1]
    value_key[reg_num] = empty_names.pop()
    value_key[reg_num].num = modify_content
def search(reg_num, reg_renaming):
    value_key = reg_renaming[1]
    if reg_num in value_key.keys():
        return value_key[reg_num]
    else:
        return 0
def del_name(reg_num, reg_renaming):
    empty_names = reg_renaming[0]
    value_key = reg_renaming[1]
    empty_names.append(value_key[reg_num])
    del value_key[reg_num]