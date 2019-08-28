import re
import os
import csv
import logging
import argparse
import datetime
    
def extract_dialogue(pathlist, regexp, result_directory):
    for books in pathlist:
        number_of_dialogues = 0
        sum_of_words_in_dialogue = 0
        
        result_txt = os.path.join(result_directory+'/'+os.path.basename(books))
        
        if os.path.exists(result_txt):
            os.remove(result_txt)
        
        with open(books, 'r') as text_file:
            for line in text_file:
                line = line.strip()
                match = re.fullmatch(regexp, line)
                if match:
                    number_of_dialogues += 1
                    sum_of_words_in_dialogue += len(match[0].split())
        
                    with open(result_txt, 'a') as result_file:
                        result_file.write(match[0])
                        result_file.write('\n')

        info = 'Source name: {}\nDestination name: {}\nDialogs: {}'.format(books, result_txt, number_of_dialogues)
        logging.info(info)

        if sum_of_words_in_dialogue == 0:
            print("no dialogues in", books)
            booklist = [os.path.basename(books), number_of_dialogues, '0']
        else:
            booklist = [os.path.basename(books), number_of_dialogues, sum_of_words_in_dialogue/number_of_dialogues]
        
        with open('stats.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(booklist)
        
        
def init_pathlist(bookpath):
    pathlist = []
    
    for dir_path, sub_dir, books in os.walk(bookpath):
        for book in books:
            if book.endswith('.txt'):
                pathlist.append(os.path.join(dir_path, book))
            
    pathlist.sort()
    return pathlist

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir', type = str, help = 'Source Directory')
    parser.add_argument('res_dir', type = str, help = 'Destination Directory')
    #parser.add_argument('regexp', type = str, default = 'reg_exp.txt', help = 'File with the regular expression')
    return parser.parse_args()    
          
def init_logger():
    text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_directory = "log/"
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)
    log_path = log_directory + text + ".log"
    logging.basicConfig(filename=log_path, level=logging.INFO, format='\n%(asctime)s\n%(message)s')

if __name__ == '__main__':
    init_logger()
    args = init_parser()	

    csvData = [['name', '#replics', 'mean']]
    with open('stats.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    
    regexp = r'(-|–|─|—).+'
    
    pathlist = init_pathlist(args.src_dir)
    extract_dialogue(pathlist = pathlist, regexp = regexp, result_directory = args.res_dir)
