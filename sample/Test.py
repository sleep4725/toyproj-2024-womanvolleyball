input_string = 'PARK SU BIN\r\n                            박수빈'

# 문자열을 '\r\n'으로 분리하고 양쪽 공백을 제거
parts = [part.strip() for part in input_string.split('\r\n')]

print(parts)