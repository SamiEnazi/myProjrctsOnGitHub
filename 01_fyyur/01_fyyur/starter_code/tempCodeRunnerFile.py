def validate_phone(self, phone,state):
        code = phone.data[3:6]
        validated = False
        
        for num in range(len(codes)):
            for number in codes[num]['code']:
                if code == number and codes[num]['name'] == state.data:
                    validated = True
                    print(state.data)
        if(validated):
            return
        else:
            raise ValidationError("Number Does not match state code!")
        