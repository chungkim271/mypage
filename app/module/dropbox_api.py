import dropbox, datetime, time

def timestamp_filename(filename):
    """ Add timestamp to a filename
    """
    split = filename.split('.')

    if len(split) > 2:
        return(filename)
    else:
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        filename_ts = split[0] + ' ' + ts + '.' + split[1]
        return(filename_ts)

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """ Upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

    def list_files(self, foldername):
        dbx = dropbox.Dropbox(self.access_token)
        
        for entry in dbx.files_list_folder(foldername).entries:
            print(entry.name)

    def delete_files(self, foldername):
        dbx = dropbox.Dropbox(self.access_token)
        dbx.files_delete(foldername)
# def main():

#     #dbx.files_delete('/test')

#     print ("Attempting to upload...")

#     filename = 'beto_in_between.jpg'
#     local_filepath = '/Users/chungkim/Desktop/'
#     dropbox_filepath = '/misclassification/'

#     file_from = local_filepath + filename
#     file_to = dropbox_filepath + timestamp_filename(filename)

#     transferData = TransferData(access_token)
#     transferData.upload_file(file_from, file_to)

#     transferData.list_files(dropbox_filepath)
#     #transferData.delete_files("/misclassification")


# if __name__ == "__main__":
#     """ This is executed when run from the command line """
#     main()
