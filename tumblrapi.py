import pytumblr

# Authenticate via OAuth
# We only need the consumer key to call "posts" function
client = pytumblr.TumblrRestClient('nAvaCgNT6dVls4dxKYnWyM1as57L0aSAkSXAayRCPEtNxJSQjr')

# Make the request
# I just created a new one to test. You can take a look how the result is going to be
print(client.posts('minkim25.tumblr.com'))


