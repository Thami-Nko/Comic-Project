import requests as req
import sys
from bs4 import BeautifulSoup
import re
import os


#First to do, fetch web url
def getComicName():
   return sys.argv[1]
   
def getVolName():
   return sys.argv[2]   
   
def getModName():
   return sys.argv[0]
 
def processImage(count_ref):
   
   img_page = req.get('https://readms.net/r/' + name_ref + '/' + vol_ref + '/6403/' + str(count_ref))  
   soup = BeautifulSoup(img_page.text, 'html.parser')
   img_tag = soup.find('img')
   image = req.get('https:' + img_tag['src'])
  

#Test function: Function will return the first image and store on pc.
def getImage(name_ref, vol_ref):

   dir_name = name_ref + ' - ' + str(vol_ref) #Directory name on local disk for comic and vol number.
   
   #Check if directory exists.
   if not os.path.exists(dir_name):
      
      #Create directory
      os.mkdir(dir_name)
      count = 1
      
      #Fetch first page.
      processImage(count)  
                
      #Download all images and save to dir
      while image.status_code != 302:
          
         with open(dir_name + '/image' + str(count) + '.jpg','wb') as file:
            
            file.write(image.content)
            print('Saving image number %d....' % (count))
            count += 1
            
            #Fetch next page
            try:
               processImage(count)
               
            except:
               print('You have saved all comics. Goodbye.')
               exit(0)   
           
   
   else:
      print('The folder "%s" already exists... Goodbye' %(name_ref))   
   
def testPage(soup_obj):
   #This function will test if a page with the specified name exists on the website.
   tag = soup_obj.find('title')
   regex = re.compile(r'page not found')
   if re.search(tag.text, regex):
      print('Webpage you are looking for does not exist. Goodbye')
      exit(0)
   else:
      print('Success!! Webpage found.')   



def getURL(name, vol=''):
   
   try:
      
      r = req.get('https://readms.net/manga/' + name)
      print(name)
      soup = BeautifulSoup(r.text, 'html.parser')
      
      testPage(soup)
      
      """
   Here we're basically creating a regex which will find the requested
   webpage via comic name and volume number
   """
      format_str = '/r/' + name + '/' + vol
      regex = re.compile(r'' + format_str)
      
      if r.status_code > 299:
         print('The page you\'re looking for does not exist')
         print('Please run the program again!!')
         exit(0)
      else:
         print('Status Code: ', r.status_code)   
         tag = soup.find(href=regex)  
         print(tag) #This finds all tags which match the regex format string. There should only be one result.
         #print(tag['href']) #You access a tag's attributes by treating it as a dictionary.
         #tag = soup.find_all(href=regex) #There should be only 1 result.
         getImage(name, vol)
         
   except:
      #print('Error: %s\nStatus Code: %s' % ('', r.status_code))
      print('Something went wrong:', e)
         
              
try:
   
   comic_name = getComicName()
   vol_name   = getVolName()
   mod_name   = getModName() 
      
   #Print variable names
   print('Details of Command Line arguments\n-------------')
   print('Comic Name: %s\nVolume Number: %s\nModule Name: %s' % (comic_name, vol_name, mod_name))
   
   #Once we've retrieved the user data. Fetch webpage using requests
   getURL(comic_name, vol_name)
   
except IndexError:
   print('You entered too few arguements. Try again')
   
# print('Your program contains the following commandline arguments:')
# print('Your name is %s and you are %s years old.' % (name, age))

   
   
