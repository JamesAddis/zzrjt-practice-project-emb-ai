''' Success messages for API/Website
'''
def success_result_message(label, score):
    ''' Generate success message from label and score
    '''
    return "The given text has been identified as {} with a score of {}".format(label, score)