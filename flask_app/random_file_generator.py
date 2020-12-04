'''
Python script to find the random file word from to files
'''

from random import choice
class RandomNameGenerator():
    def extract_name(self,fn):
        with open(fn,'r') as readfile:
            name = choice(readfile.readlines())
            return choice(name.strip().split(','))
    def generate_random(self):
        file_name1 = "noun_list.csv"
        file_name2 = 'most-common-verbs-english.csv'
        noun_name = self.extract_name(file_name1)
        verb_name = self.extract_name(file_name2)
        return (noun_name,verb_name)
    

       
if __name__ == "__main__":
    web_link = RandomNameGenerator()
    print(web_link.generate_random())
  