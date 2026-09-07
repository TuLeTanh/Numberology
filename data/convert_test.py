import sys

sys.stdout.reconfigure(encoding='utf-8')

VNI_MAP = {
    'aù': 'á', 'aø': 'à', 'aû': 'ả', 'aõ': 'ã', 'aï': 'ạ',
    'aâ': 'â', 'aá': 'ấ', 'aà': 'ầ', 'aå': 'ẩ', 'aã': 'ẫ', 'aä': 'ậ',
    'aê': 'ă', 'aé': 'ắ', 'aè': 'ằ', 'aú': 'ẳ', 'añ': 'ẵ', 'aö': 'ặ',
    
    'AÙ': 'Á', 'AØ': 'À', 'AÛ': 'Ả', 'AÕ': 'Ã', 'AÏ': 'Ạ',
    'AÂ': 'Â', 'AÁ': 'Ấ', 'AÀ': 'Ầ', 'AÅ': 'Ẩ', 'AÃ': 'Ẫ', 'AÄ': 'Ậ',
    'AÊ': 'Ă', 'AÉ': 'Ắ', 'AÈ': 'Ằ', 'AÚ': 'Ẳ', 'AÑ': 'Ẵ', 'AÖ': 'Ặ',

    'Aù': 'Á', 'Aø': 'À', 'Aû': 'Ả', 'Aõ': 'Ã', 'Aï': 'Ạ',
    'Aâ': 'Â', 'Aá': 'Ấ', 'Aà': 'Ầ', 'Aå': 'Ẩ', 'Aã': 'Ẫ', 'Aä': 'Ậ',
    'Aê': 'Ă', 'Aé': 'Ắ', 'Aè': 'Ằ', 'Aú': 'Ẳ', 'Añ': 'Ẵ', 'Aö': 'Ặ',
    
    'eù': 'é', 'eø': 'è', 'eû': 'ẻ', 'eõ': 'ẽ', 'eï': 'ẹ',
    'eâ': 'ê', 'eá': 'ế', 'eà': 'ề', 'eå': 'ể', 'eã': 'ễ', 'eä': 'ệ',
    
    'EÙ': 'É', 'EØ': 'È', 'EÛ': 'Ẻ', 'EÕ': 'Ẽ', 'EÏ': 'Ẹ',
    'EÂ': 'Ê', 'EÁ': 'Ế', 'EÀ': 'Ề', 'EÅ': 'Ể', 'EÃ': 'Ễ', 'EÄ': 'Ệ',
    
    'Eù': 'É', 'Eø': 'È', 'Eû': 'Ẻ', 'Eõ': 'Ẽ', 'Eï': 'Ẹ',
    'Eâ': 'Ê', 'Eá': 'Ế', 'Eà': 'Ề', 'Eå': 'Ể', 'Eã': 'Ễ', 'Eä': 'Ệ',
    
    'où': 'ó', 'oø': 'ò', 'oû': 'ỏ', 'oõ': 'õ', 'oï': 'ọ',
    'oâ': 'ô', 'oá': 'ố', 'oà': 'ồ', 'oå': 'ổ', 'oã': 'ỗ', 'oä': 'ộ',
    
    'OÙ': 'Ó', 'OØ': 'Ò', 'OÛ': 'Ỏ', 'OÕ': 'Õ', 'OÏ': 'Ọ',
    'OÂ': 'Ô', 'OÁ': 'Ố', 'OÀ': 'Ồ', 'OÅ': 'Ổ', 'OÃ': 'Ỗ', 'OÄ': 'Ộ',
    
    'Où': 'Ó', 'Oø': 'Ò', 'Oû': 'Ỏ', 'Oõ': 'Õ', 'Oï': 'Ọ',
    'Oâ': 'Ô', 'Oá': 'Ố', 'Oà': 'Ồ', 'Oå': 'Ổ', 'Oã': 'Ỗ', 'Oä': 'Ộ',
    
    'uù': 'ú', 'uø': 'ù', 'uû': 'ủ', 'uõ': 'ũ', 'uï': 'ụ',
    
    'UÙ': 'Ú', 'UØ': 'Ù', 'UÛ': 'Ủ', 'UÕ': 'Ũ', 'UÏ': 'Ụ',
    'Uù': 'Ú', 'Uø': 'Ù', 'Uû': 'Ủ', 'Uõ': 'Ũ', 'Uï': 'Ụ',
    
    'iù': 'í', 'iø': 'ì', 'iû': 'ỉ', 'iõ': 'ĩ', 'iï': 'ị',
    
    'IÙ': 'Í', 'IØ': 'Ì', 'IÛ': 'Ỉ', 'IÕ': 'Ĩ', 'IÏ': 'Ị',
    'Iù': 'Í', 'Iø': 'Ì', 'Iû': 'Ỉ', 'Iõ': 'Ĩ', 'Iï': 'Ị',
    
    'yù': 'ý', 'yø': 'ỳ', 'yû': 'ỷ', 'yõ': 'ỹ', 'yï': 'ỵ',
    
    'YÙ': 'Ý', 'YØ': 'Ỳ', 'YÛ': 'Ỷ', 'YÕ': 'Ỹ', 'YÏ': 'Ỵ',
    'Yù': 'Ý', 'Yø': 'Ỳ', 'Yû': 'Ỷ', 'Yõ': 'Ỹ', 'Yï': 'Ỵ',
    
    'ôù': 'ớ', 'ôø': 'ờ', 'ôû': 'ở', 'ôõ': 'ỡ', 'ôï': 'ợ',
    'öù': 'ứ', 'öø': 'ừ', 'öû': 'ử', 'öõ': 'ữ', 'öï': 'ự',
    
    'ÔÙ': 'Ớ', 'ÔØ': 'Ờ', 'ÔÛ': 'Ở', 'ÔÕ': 'Ỡ', 'ÔÏ': 'Ợ',
    'ÖÙ': 'Ứ', 'ÖØ': 'Ừ', 'ÖÛ': 'Ử', 'ÖÕ': 'Ữ', 'ÖÏ': 'Ự',
    
    'Ôù': 'Ớ', 'Ôø': 'Ờ', 'Ôû': 'Ở', 'Ôõ': 'Ỡ', 'Ôï': 'Ợ',
    'Öù': 'Ứ', 'Öø': 'Ừ', 'Öû': 'Ử', 'Öõ': 'Ữ', 'Öï': 'Ự',

    'ô': 'ơ', 'ö': 'ư',
    'Ô': 'Ơ', 'Ö': 'Ư',
    'ñ': 'đ', 'Ñ': 'Đ'
}

def vni_to_unicode(text):
    keys = sorted(VNI_MAP.keys(), key=lambda x: len(x), reverse=True)
    result = ""
    i = 0
    while i < len(text):
        match = None
        for k in keys:
            if text.startswith(k, i):
                match = k
                break
        if match:
            result += VNI_MAP[match]
            i += len(match)
        else:
            result += text[i]
            i += 1
            
    # Fix misplaced tones
    result = result.replace('ÒA', 'OÀ').replace('òA', 'oÀ').replace('Òa', 'Oà').replace('òa', 'oà')
    result = result.replace('ÓA', 'OÁ').replace('óa', 'oá').replace('Óa', 'Oá').replace('óA', 'oÁ')
    result = result.replace('ỎA', 'OẢ').replace('ỏa', 'oả')
    result = result.replace('ÕA', 'OÃ').replace('õa', 'oã')
    result = result.replace('ỌA', 'OẠ').replace('ọa', 'oạ')
    
    result = result.replace('ÚY', 'UÝ').replace('úy', 'uý')
    result = result.replace('ÙY', 'UỲ').replace('ùy', 'uỳ')
    result = result.replace('ỦY', 'UỶ').replace('ủy', 'uỷ')
    result = result.replace('ŨY', 'UỸ').replace('ũy', 'uỹ')
    result = result.replace('ỤY', 'UỴ').replace('ụy', 'uỵ')
    
    return result

tc1 = "TÖÛ VI ÑAÅU SOÁ TOØAN THÖ – Vuõ Taøi Luïc"
exp1 = "TỬ VI ĐẨU SỐ TOÀN THƯ – Vũ Tài Lục"
r1 = vni_to_unicode(tc1)
print(f"TC1 match: {r1 == exp1}")
print(f"Result: '{r1}'")
print(f"Expect: '{exp1}'")
if r1 != exp1:
    for i in range(len(r1)):
        if i >= len(exp1) or r1[i] != exp1[i]:
            print(f"Mismatch at index {i}: '{r1[i]}' vs '{exp1[i] if i<len(exp1) else ''}'")
            break

tc2 = "Nhöng meänh lyù chaúng nhöõng noù luoân luoân khoâng gioáng thöôøng lyù"
exp2 = "Nhưng mệnh lý chẳng những nó luôn luôn không giống thường lý"
r2 = vni_to_unicode(tc2)
print(f"TC2 match: {r2 == exp2}")
print(f"Result: '{r2}'")
print(f"Expect: '{exp2}'")
