setInput = ''
socketStatus = 'unknown'
sensorStatus = 'unknown'
cameraStatus = 'unknown'
buttonStatus = 'unknown'

# Start all modules here:


            # TO ADD.





print('\n \n----------------------------------------------------------')

print('YENGA v 0.1')
print('\n Program initiated:')
print('Socket status: ' + str(socketStatus))
print('Sensor status: ' + str(sensorStatus))
print('Camera status: ' + str(cameraStatus))
print('Button status: ' + str(buttonStatus))

print('----------------------------------------------------------\n')

setInput = input('Please set input: ')

while ( setInput != 'exit'):

    if (setInput == 'pvg'):
        
        # This is player vs game. Computer makes a move, then players makes a move and presses button and so on, until someone wins.
        

        print('\n----------------------------------------------------------')
        print('----------------------------------------------------------\n')
        print('\nWelcome to player - vs - game !')
        print('\nPlease wait for computer to make a move, after that you make a move and when finished press the button to let computer know it is its time again.\n')

        while ( setInput != 'exit' and setInput != 'end'):
            
            # This is the actual program loop, it will keep running until the game is finished.
            print('loop')







    if (setInput == 'pvp'):

        # This is a player vs player mode, with a twist. Players take turns in choosing which block robot pulls out.

        print('\n----------------------------------------------------------')
        print('----------------------------------------------------------\n')
        print('\nWelcome to player - vs - player !')
        print('\nThis is a player vs player mode, with a twist. Players take turns in choosing which block robot pulls out.\n')


    setInput = input('\nPlease set input: ')

