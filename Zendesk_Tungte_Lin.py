import json
import math
import requests
import unittest

#sToken='Cbbe008boKpXDzNFUcRcqvPje43Niv4wendBU6iR'
aCredentials    = 'littlethe2000@yahoo.com.tw', 'little2380'
#aCredentials    = 'little2000@yahoo.com.tw/token', 'Cbbe008boKpXDzNFUcRcqvPje43Niv4wendBU6iR'
sUrlTicket      = f'https://zcctungte.zendesk.com/api/v2/tickets'
sUrlUsers       = f'https://zcctungte.zendesk.com/api/v2/users/show_many.json?ids='
session         = requests.Session()
session.auth    = aCredentials
sOutputBlock1   = '{:6}'
sOutputBlock2   = '{:60}'
sOutputBlock3   = '{:>20}'

# Unit tests by the standard unit testing framework(unittest). Testing targets are 2 functions: checkInput() and showTicket().
class DictTest(unittest.TestCase):
    
    def testCheckInputLetter(self):
        iInput=checkInput('a',0,1)
        self.assertEqual(iInput,-1)
        
    def testCheckInputEmpty(self):
        iInput=checkInput('',0,1)
        self.assertEqual(iInput,-1)

    def testCheckInputNumber(self):
        iInput=checkInput('0',0,1)
        self.assertEqual(iInput,0)

    def testCheckInputOutOfRange(self):
        iInput=checkInput('2',0,1)
        self.assertEqual(iInput,-1)

    def testShowTicketType(self):
        with self.assertRaises(TypeError):
            showTicket('',True)

# checkInput() is used to check the input string is valid or not. The input string should be an option('r' or a number).
def checkInput(sInput,iMin,iMax):
    print('\n')
    bInt=True
    iInput=-1
    try:
        iInput = int(sInput)
    except ValueError:
        bInt=False
    if(bInt):
        if(iInput > iMax or iInput < iMin):
            print('Please input a number between '+str(iMin)+' and '+str(iMax)+'\n')
            return -1
        else:
            return iInput
    else:
        print('Please input a number or a valid option.\n')
        return -1

# showTicket() is for displaying the content of one ticket. If bShowDetail is false, the content displaying is only for a list of tickets.
def showTicket(dictTicket,bShowDetail):
    if(bShowDetail):
        oResponse = session.get(sUrlUsers+str(dictTicket['requester_id'])+','+str(dictTicket['assignee_id'])+','+str(dictTicket['submitter_id']))
        if(oResponse.status_code == 200):
            dictResult=oResponse.json()
            arrayUsers=dictResult['users']
            
            for dictUser in arrayUsers:
                if(dictUser['id']==dictTicket['requester_id']):
                    dictTicket['requester_name']=dictUser['name']
                if(dictUser['id']==dictTicket['submitter_id']):
                    dictTicket['submitter_name']=dictUser['name']
                if(dictUser['id']==dictTicket['assignee_id']):
                    dictTicket['assignee_name']=dictUser['name']
            print('Ticket ID:\t',dictTicket['id'])
            print('Subject:\t',dictTicket['subject'])
            print('Requester Name:\t',dictTicket['requester_name'])
            print('Assignee Name:\t',dictTicket['assignee_name'])
            print('Submitter Name:\t',dictTicket['submitter_name'])
            print('Updated Time:\t',dictTicket['updated_at'])
            print('Created Time:\t',dictTicket['created_at'])
            print('Description:\n')
            print(dictTicket['description']+'\n')
            sSeparator=','
            sTags=sSeparator.join(dictTicket['tags'])
            print('Tags:'+sTags)
        else:
            print('The request of users is not available. Status Code:',oResponse.status_code,'\n')
    else:
            print(sOutputBlock1.format(str(dictTicket['id']))+sOutputBlock2.format(dictTicket['subject'])+sOutputBlock3.format(dictTicket['updated_at']))

# viewPage() is the menu for viewing pages. Pressing 'r' can see the detail of a ticket.
def viewPage():
    while(1):
        oResponse = session.get(sUrlTicket+'/count.json')
        if(oResponse.status_code == 200):
            dictResult=oResponse.json()
            iTotalTickets=dictResult['count']['value']
            print('The number of total tickets is '+str(iTotalTickets)+'.')
            iTotalAPIPages=math.ceil(iTotalTickets/100)
            print('There is(are) '+str(iTotalAPIPages)+' page(s).')
            print('Input the page number 1-'+str(iTotalAPIPages)+' to read the page.')
            print('Or, input 0 to go back to the main menu.')
            print('Or, input r to read the detail of a ticket.')            

            sInput=input()
            if(sInput=='r' or sInput=='R'):
                print('\n')
                viewDetail()
            else:
                iInput=checkInput(sInput,0,iTotalAPIPages)
                
                if(iInput ==0):
                    return
                else:
                    oResponse = session.get(sUrlTicket+'.json?page='+str(iInput))
                    if(oResponse.status_code == 200):
                        dictTickets=oResponse.json()
                        arrayTickets=dictTickets['tickets']
                        print(sOutputBlock1.format('ID')+sOutputBlock2.format('Subject')+sOutputBlock3.format('Updated Time'))
                        for dictTicket in arrayTickets:
                            showTicket(dictTicket,False)
                        print('\n')
                    else:
                        print('The request of tickets(pages) is not available. Status Code:',oResponse.status_code,'\n')
                        return
                        
        else:
            print('The request of tickets(count) is not available. Status Code:',oResponse.status_code,'\n')
            return

# viewDetail() is displaying the question to ask the user which ticket he wants to see.
def viewDetail():
    while(1):
        print('Please input the ticket ID to view the detail, or input 0 to quit:')
        sInput=input()
        print('\n')
        if(sInput=='0'):
            return
        elif(sInput != -1):
            oResponse = session.get(sUrlTicket+'/'+sInput+'.json')
            if(oResponse.status_code == 200):
                dictResult=oResponse.json()
                showTicket(dictResult['ticket'],True)
                print('\n')
            else:
                print('The request of the ticket is not available. Status Code:',oResponse.status_code,'\n')
                
# The main function and the main menu. The entrance of this application. Unit tests can be runned here.
def main():
    while(1):
        print('Welcome to Zendesk ticket veiwer.\n')     
        print('1.View tickets from Zendesk API.')
        print('2.Run unit tests.')
        print('0.Exit.')         
        print('Please input the option(0-2):')
        iInput=checkInput(input(),0,2)

        if(iInput==1):
            viewPage()
        if(iInput==2):
            unittest.main()
        elif(iInput==0):
            print('Bye.')
            exit()

# Calling the main function.
if __name__ == "__main__":
    main()


