#! /usr/bin/python3.6
#! -*- coding: utf-8 -*-


# #############################################################################
# standard phyton modules
# #############################################################################
import os            # standard os lib
import sys           # standard sys lib
import csv           # standard csv lib for csv file I/O
import zipfile

# #############################################################################
# constants, global variables
# #############################################################################
NAME = __file__
SPLIT_DIR = os.path.dirname(os.path.realpath(NAME))
SCRIPT_DIR = SPLIT_DIR + '/.' + os.path.basename(NAME)
LIB_DIR = SCRIPT_DIR + '/cache/lib/'
sys.path.insert(0, LIB_DIR)

# #############################################################################
# Third party phyton modules - list with procedure to install and import them
# #############################################################################
# After first installation check for rigth package name in LIB_DIR for third column
# Bug for third party libs - workaround - After first installation it need to rerun the script.
# Don't know why, still under investigation.
import_list = [
   ('lxml',       '4.2.1', 'lxml-4.2.1.dist-info')              # XML toolkit
]

for line in import_list:
   try:
      if os.path.isdir(LIB_DIR+line[2]):
         #print('Found installed '+line[0]+line[1]+' in '+line[2])
         pass
      else:
         try:
            import pip
         except:
            print("For debian - Use sudo apt-get install python3-pip")
            print("For centos/redhat - use  yum -y install python36u-pip")
            #TO DO - change script to use get-pip unless installing pip as root
            # Probably solution for problem with installing pip.
            # https://github.com/pypa/get-pip
            sys.exit(1)
         print('No lib '+line[0]+'-'+line[1])
         os.system("python"+sys.version[0:3]+" -m pip install '"+line[0]+'=='+line[1]+"' --target="+LIB_DIR)
      module_obj = __import__(line[0])
      globals()[line[0]] = module_obj
   except ImportError as e:
      print(line[0]+' is not installed')

# #############################################################################
# functions
# #############################################################################

def unzip(path):
   with zipfile.ZipFile(path,"r") as zip_ref:
      zip_ref.extractall(os.path.dirname(os.path.realpath(path)))
      return zipfile.ZipFile.namelist(zip_ref)

def read_xml_file(path):
   '''
   XML file reader.
   '''
   try:
      tree = etree.parse(path)
      root = tree.getroot()
      return root
   except IOError as e:
      print('Problem with file or filepath.')
      print(e)

def csv_write(file_name, limit, data):
   '''
   CSV write example.
   '''
   if isinstance(data, str):
      data = data.split('\n')
   with open(file_name, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile, delimiter=limit)
      for line in data:
         writer.writerow(line)

def opt_write_csv(file_name):
   data = [['asd','gfadfgd','fgarsdfgf'],
             ['qae','qwr','wer'],
             ['line3','1','2'],
             ['line4','4','#comment']]
   csv_write(file_name,';',data)

# #############################################################################
# main app function - reading arguments with argpars
# #############################################################################

def main():
   zip_path = sys.argv[1]
   #Założenie, że w zipie jest zawsze tylko plik.
   unziped = os.path.dirname(os.path.realpath(sys.argv[1])) + '/' + unzip(zip_path)[0]
   print(unziped)
   xml_tree = read_xml_file(unziped)
   print(etree.tostring(xml_tree, pretty_print=True).decode('ascii'))



if __name__ == '__main__':
   from lxml import etree
   main()
