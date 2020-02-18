import piethon
import time
import sys

def convert():
    #open both files to read and write
    write_file = open("piethon.py", "w")
    read_file = open("userUploadPie.py", "r")

    #parse through the read file string and replace the print statements
    #output_list.append(what was in the print statement)
    #also adds tabs in front of every line
    read_file_deprint = read_file.read()
    read_file_deprint = read_file_deprint.replace("print(", "output_list.append(")
    read_file_deprint = read_file_deprint.replace("\n", "\n\t")
    read_file_deprint = read_file_deprint.replace("`", "")
    read_file_deprint = "\t" + read_file_deprint
    print("converting: ", read_file_deprint)

    #declaring other lines that must go in the output file
    function_str = "def userGenerated():\n"
    output_list_str = "\toutput_list = []\n"
    return_statement = "\n\treturn output_list\n"

    #combine all of the strings into a list and then insert them into the output file
    L = [function_str, output_list_str, read_file_deprint, return_statement]
    write_file.writelines(L)

    write_file.flush()
    sys.stdout.flush()
    time.sleep(1)

    output_list = piethon.userGenerated()
    print(output_list)
    return output_list

if __name__ == '__main__':
    convert()