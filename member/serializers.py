from rest_framework import serializers
from .models import Member
from django.contrib.auth.hashers import make_password

class MemberRegisterSerializer(serializers.ModelSerializer):
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Too Short Password') # 여기서 바로 json으로 에러 메시지 내보냄. 즉 validate메서드 호출 안 함.
        return make_password(value)
    
    def validate(self, data): 
        # 데이터 확인용...       
        print('MemberRegisterSerializer - validate called.')
        for key, value in data.items():
            print(f'@@@ key: {key}, value: {value}')
        return data
    
    class Meta:
        model = Member
        fields = ('id', 'username', 'password', 'tel')
        extra_kwargs = {
            'id': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
            },
        }
        
    #     MemberRegisterSerializer():
    # username = CharField(help_text='150자 이하 문자, 숫자 그리고 @/./+/-/_만 가능합니다.', label='사용자 이름', max_length=150, validators=[<django.contrib.auth.validators.UnicodeUsernameValidator object>, <UniqueValidator(queryset=Member.objects.all())>])
    # password = CharField(label='비밀번호', max_length=128, write_only=True)
    # tel = CharField(allow_blank=True, allow_null=True, label='연락처', max_length=64, required=False)
