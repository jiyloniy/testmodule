from twilio.rest import Client

account_sid = 'AC88cc475a81ea89f5377a7453ce549a5c'
# 668f640f6426d1c731f2a3f692848fce
auth_token = '668f640f6426d1c731f2a3f692848fce'
client = Client(account_sid, auth_token)

my_phone = '+16506514720'

message = client.messages.create(
    body='Abrordev!',
    from_='+16506514720',
    to='+998500049297'
)
print(message.sid)
