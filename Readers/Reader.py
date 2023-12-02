
class Reader:
    @staticmethod
    def is_email_valid(email):
        if email.count('@') == 1:
            split_mail_by_at = email.split('@')

            if len(split_mail_by_at[0]) > 0:
                second_half_split_by_dot = split_mail_by_at[1].split('.')

                if len(second_half_split_by_dot[0]) > 0:
                    if (4 > len(second_half_split_by_dot[-1]) > 1) and second_half_split_by_dot[-1].isalnum():
                        return True

        return False

    @staticmethod
    def validate_phone_numbers(phone_num):

        if len(phone_num) == 9:
            return phone_num

        new_num = phone_num.replace('+48', '').replace('(48)', '').replace(' ', '')
        new_num = str(int(new_num))[:9]

        return new_num

    def is_record_initially_invalid(self, record_data):
        return record_data[1] == '' or not self.is_email_valid(record_data[2])
