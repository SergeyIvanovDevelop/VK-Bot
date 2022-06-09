# -*- coding: utf-8 -*-

import vk_api
import requests

my_token = '<your_group_token>' # группа
my_token_2 = '<your_app_token>' # приложение

def captcha_handler(captcha):
    """ При возникновении капчи вызывается эта функция и ей передается объект
        капчи. Через метод get_url можно получить ссылку на изображение.
        Через метод try_again можно попытаться отправить запрос с кодом капчи
    """
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)

import random
friend_id = []
session = requests.Session()
login, password = '<phone_number>', '<password>'
vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
#vk_session = vk_api.VkApi(token='<your_app_token>',  captcha_handler=captcha_handler)
vk = vk_session.get_api()
try:
    vk_session.auth(token_only=True)  # функция для обработки капчи
    with vk_api.VkRequestsPool(vk_session) as pool:
      friends = pool.method('friends.get')
      status = pool.method('status.get')
    print("good come in")
    friend_id = friends.result['items']
    print("my_friends_id = ", friend_id)
except vk_api.AuthError as error_msg:
    print(error_msg)
    print("error")

def get_user_id (id):
  vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler)
#vk_session = vk_api.VkApi(token='<your_app_token>',  captcha_handler=captcha_handler)
  vk = vk_session.get_api()
  try:
    vk_session.auth(token_only=True)  # функция для обработки капчи
    friends_ids = []
    with vk_api.VkRequestsPool(vk_session) as pool:
      friends_ids = pool.method('friends.get', {'user_id' : id})
    friend_ids = friends_ids.result['items']
    return friend_ids
  except vk_api.AuthError as error_msg:
    print(error_msg)
    print("error")

vk_session = vk_api.VkApi(token='<your_group_token>')

import random
#longpool
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:
        print("event.user_id = ", event.user_id)
        if event.user_id == '<group_owner_id>':			
        #if True: #event.text == 'Первый вариант фразы' or event.text == 'Второй вариант фразы': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                # Получаем список всех друзей
                print("Incoming message")
                result = vk_session.method("messages.getById", {
                        "message_ids": [event.message_id],
                        "group_id": '<group_id>'
                    })
                print("result = ", result)
                print("result['items']['attachments'] = ", result['items'][0]['attachments'])

                att = result['items'][0]['attachments']
                att_size = len(att)
                print("att_size = ", att_size)

                if att_size!=0:
                  attachments = []
                else:
                  attachments = None

                for i in range(0, att_size):
                  print("att[" + str(i) + "] = " + str(att[i]))
                  print("att[" + str(i) + "] = " + str(att[i]['type']))
                  type_add = str(att[i]['type'])
                  adding_1 = att[i][type_add]
                  if type_add!="audio":
                    string_add = type_add + "{}_{}_{}"
                    adding_2 = string_add.format(adding_1['owner_id'], adding_1['id'], adding_1['access_key'])
                  else:
                    string_add = type_add + "{}_{}"
                    adding_2 = string_add.format(adding_1['owner_id'], adding_1['id'])  
                  attachments.append(adding_2)

                '''
                try:
                    photo = result['items'][0]['attachments'][0]['photo']
                    attachment = "photo{}_{}_{}".format(photo['owner_id'], photo['id'], photo['access_key'])
                except:
                    attachment = None
                '''

                result_member = vk_session.method("groups.getMembers", {
                        "group_id": '<group_id>'
                    })

                print("result_member = ", result_member['items'])
                result_member_list = result_member['items']
                text = event.text

                # тот список, по которому будет осуществляться рассылка
                send_user_list = []

                if text[0] == "1":
                  send_user_list = friend_id
                  print("Текст начинается с 1")
                  new_text = text[1:]

                elif text[0] == "2":
                  id  = int(text[2:11])
                  print("id = ", id)                 
                  send_user_list = get_user_id (id) # Id введенного человека
                  print("Друзья по id: ", send_user_list)
                  print("Текст начинается с 2")
                  new_text = text[12:]
                
                elif text[0] == "3":
                  send_user_list = result_member_list 

                else:
                  send_user_list = ['<group_owner_id>'] 
                  print("Неизвестный текст")
                  #new_text = "Неизвестое сообщение от id = '" + str(event.user_id) + "' :"  + text[:]
                  new_text = "Неизвестое сообщение (неразобрана команда): " + text[:]
                print("Текст, который будет всем рассылаться: ", new_text)     

		 # Вручную для отладки можно конкретных людей указать
                new_list_user_id = ['<user1_id>', '<user2_id>'] # ['<user3_id>'] 
                for id in new_list_user_id: # # его необходимо потом будет заменить на send_user_list
                    try:
                        vk.messages.send(user_id=id, attachment=attachments, random_id = random.randint(1,10000), message=new_text)
                    except:
                        error_string = "Пользователь с id = " + str(id) + " ограничил доступ к личным сообщениям."
                        print(error_string)
            #elif event.from_chat: #Если написали в Беседе
            #    vk.messages.send( #Отправляем собщение
            #        chat_id=event.chat_id,
            #        message='Ваш текст'
		#)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id != '<group_owner_id>':
          if event.from_user:
            know_messages = ["Привет", "привет", "Узнать стоимость", "Обо мне", "Записаться на фотосессию", "Посмотреть примеры работ"]
            string_price = "<your_price_str>"
            string_about_me = "<your_about_str>" 
            string_order_photo = "<your_string_order_photo>"
            string_example_photo = "<your_string_example_photo>"

            have = False
            sentence = None
            for sentences in know_messages:
              if sentences==event.text:
                sentence = event.text
                have = True

            if have == True:
              if sentence == "Узнать стоимость":
                vk.messages.send(
                        user_id=event.user_id,
                        message=string_price,
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )
              if sentence == "Обо мне":
                vk.messages.send(
                        user_id=event.user_id,
                        message=string_about_me,
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )
              if sentence == "Записаться на фотосессию":
                vk.messages.send(
                        user_id=event.user_id,
                        message=string_order_photo,
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    ) 
                string_order_photo2 = "Владелец, этот человек: id [" + str(event.user_id) +  "] " +  "хочет заказать у тебя фотосъемку. Свяжись с ним😉"    
                vk.messages.send(
                        user_id='<group_owner_id>',
                        message=string_order_photo2,
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )  
              if sentence == "Посмотреть примеры работ":
                vk.messages.send(
                        user_id=event.user_id,
                        message=string_example_photo,
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )

              if event.text=="Привет" or event.text=="привет" or event.text == "Здравствуйте" or event.text == "здравствуйте":
                vk.messages.send(
                        user_id=event.user_id,
                        message="Приветствуем Вас в нашем сообществе! Что Вас интересует?",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )
            else:
                vk.messages.send(
                        user_id='<group_owner_id>',
                        message="Говорит БОТ: Пользователь с id = " + str(event.user_id) + " написал сообщение неизвестного типа: '" + str(event.text) + "'.",
                        random_id=random.randint(1,10000)
                    )   
                vk.messages.send(
                        user_id=event.user_id,
                        message="Я Бот этого сообщества. Пожалуйста, выберите то, что Вас интересует в интерактивном меню или дождитесь пока Вам ответит администратор.",
                        keyboard=open("keyboard.json", "r", encoding="UTF-8").read(),
                        random_id=random.randint(1,10000)
                    )           
    print('Бот словил событие!')
