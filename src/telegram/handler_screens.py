import sys
import json
from telebot import types
from telebot import types
import telebot
state_users = {}
select_users = {}


class StateUser():
    def __init__(self, step_id):
        self.step_id = step_id


def get_all_answers():
    answers = {}
    with open(sys.path[0] + '/src/telegram/screens.json', 'r') as file:
        answers = json.load(file)
    return answers


def get_text_message(message_id):
    answers = get_all_answers()
    all_messages = answers['elements'][0]['messages']
    for message in all_messages:
        if message['message_id'] == message_id:
            text_message = message['text']
            return text_message


def get_text_button(button_id):
    answers = get_all_answers()
    all_buttons = answers['elements'][0]['buttons']
    for button in all_buttons:
        if button['button_id'] == button_id:
            button_message = button['text']
            return button_message


def get_keyboard_answer(buttons):
    # Attention! NEED TEST! NOW WORKING FOR CORRENT CASES
    keyboard = types.ReplyKeyboardMarkup()
    if len(buttons) % 3 == 0:
        for i in range(len(buttons) // 3):
            button_id1 = buttons[i]['button_id']
            button_id2 = buttons[len(buttons) - 1 - i]['button_id']
            button_id3 = buttons[len(buttons) - 3 - i]['button_id']
            button_message1 = get_text_button(button_id1)
            button_message2 = get_text_button(button_id2)
            button_message3 = get_text_button(button_id3)
            keyboard.add(button_message1, button_message2, button_message3)
    elif len(buttons) % 2 == 0:
        for i in range(len(buttons) // 2):
            button_id1 = buttons[i]['button_id']
            button_id2 = buttons[len(buttons) - i - 1]['button_id']
            button_message1 = get_text_button(button_id1)
            button_message2 = get_text_button(button_id2)
            keyboard.add(button_message1, button_message2)
    else:
        if len(buttons) > 6:
            remains = len(buttons) - (len(buttons) // 3)
            for i in range(len(buttons) // 3):
                button_id1 = buttons[i]['button_id']
                button_id2 = buttons[len(buttons) - 1 - i]['button_id']
                button_id3 = buttons[len(buttons) - 3 - i]['button_id']
                button_message1 = get_text_button(button_id1)
                button_message2 = get_text_button(button_id2)
                button_message3 = get_text_button(button_id3)
                keyboard.add(button_message1, button_message2, button_message3)
            if remains % 2 == 0:
                button_id1 = buttons[len(buttons) - 1]['button_id']
                button_id2 = buttons[len(buttons) - 2]['button_id']
                button_message1 = get_text_button(button_id1)
                button_message2 = get_text_button(button_id2)
                keyboard.add(button_message1, button_message2)
            else:
                button_id1 = buttons[len(buttons) - 1]['button_id']
                button_message1 = get_text_button(button_id1)
                keyboard.add(button_message1, button_message2)
        else:
            remains = len(buttons) - ((len(buttons) // 2) * 2)
            remain_button = buttons[len(buttons) - 1]
            buttons = buttons[0:len(buttons)-1]
            for i in range(len(buttons) // 2):
                button_id1 = buttons[i]['button_id']
                button_id2 = buttons[len(buttons) - 1 - i]['button_id']
                print(button_id1, button_id2)
                button_message1 = get_text_button(button_id1)
                button_message2 = get_text_button(button_id2)
                keyboard.add(button_message1, button_message2)
            button_id1 = remain_button['button_id']
            print(button_id1)
            button_message1 = get_text_button(button_id1)
            keyboard.add(button_message1)
    return keyboard


def get_answer(step_id):
    answers = get_all_answers()
    for action in answers['actions']:
        if action['step_id'] == step_id:
            message_id = action['message_id']
            text_message = get_text_message(message_id)
            buttons = action['buttons']
            keyboard = get_keyboard_answer(buttons)
            return (text_message, keyboard)


def check_message(message, step_id):
    answers = get_all_answers()
    for action in answers['actions']:
        if action['step_id'] == step_id:
            for button in action['buttons']:
                text_button = get_text_button(button['button_id'])
                if text_button == message:
                    return True
            return False


def get_next_step_id(step_id, message):
    answers = get_all_answers()
    for action in answers['actions']:
        if action['step_id'] == step_id:
            for button in action['buttons']:
                button_text = get_text_button(button['button_id'])
                if button_text == message:
                    try:
                        next_step_id = button['next_step_id']
                        return next_step_id
                    except:
                        return None


def save_change_user(now_state, user_id, message):
    users_record = select_users.get(user_id, [])
    if now_state == 1 or now_state == 3 or now_state == 4 or now_state == 2:
        if len(users_record) == 2:
            users_record[1] = message
        else:
            users_record.append(message)
        select_users.update({user_id: users_record})

    if message == 'back':
        select_users.update({user_id: []})
    print(select_users)


def get_next_screen(user_id, message):
    now_state = state_users.get(user_id, -1)
    if now_state == -1:
        answer = get_answer(0)
        state_users.update({user_id: 0})
        return answer
    is_correct_message = check_message(message, now_state)
    next_step_id = get_next_step_id(now_state, message)
    if is_correct_message:
        save_change_user(now_state, user_id, message)
        print(next_step_id)
        if next_step_id is None:
            answer = get_answer(now_state)
            return ('photo', answer[1])
        answer = get_answer(next_step_id)
        state_users.update({user_id: next_step_id})
        return answer
    answer = get_answer(0)
    text_answer = 'Invalid data '
    state_users.pop(user_id)
    return (text_answer + answer[0], answer[1])


def get_user_select(user_id):
    select = select_users[user_id]
    if select[0] in ['RSI', 'MACD', 'SMA', 'EMA']:
        print('qqqq')
        tmp = select[0]
        select[0] = select[1]
        select[1] = tmp
    return select
