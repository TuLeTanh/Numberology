import json
import os

data = {
    "_metadata": {
        "phien_ban": "2.0",
        "nguon_goc": "Từ Điển Tử Vi Đẩu Số & Thần Số Học - Biên soạn mới chuẩn hệ thống Pythagorean (Tham khảo: David A. Phillips, Faith Javane, WorldNumerology)"
    },
    
    "duong_doi": {
        "_description": "Life Path Number - Dựa trên tổng ngày tháng năm sinh (Hành trình và bài học cốt lõi)",
        "1": { 
            "y_nghia_tong_quat": "Đường đời 1 là con đường của sự độc lập, tiên phong và rèn luyện bản lĩnh cá nhân. Bài học lớn nhất của bạn là học cách tự đứng trên đôi chân của mình, bứt phá khỏi đám đông và trở thành người dẫn dắt.", 
            "diem_manh": "Tự tin, quyết đoán, có tư duy sáng tạo độc lập, ý chí kiên cường và khả năng lãnh đạo bẩm sinh.", 
            "diem_yeu": "Dễ trở nên ích kỷ, độc đoán, thiếu kiên nhẫn với người chậm hơn mình, và đôi khi quá bảo thủ, bướng bỉnh." 
        },
        "2": { 
            "y_nghia_tong_quat": "Đường đời 2 là con đường của sự hòa giải, hợp tác và thấu hiểu. Bài học của bạn là tạo ra sự hài hòa, làm cầu nối gắn kết mọi người và phát triển sức mạnh từ sự tĩnh lặng, nhẫn nại.", 
            "diem_manh": "Tế nhị, ngoại giao xuất sắc, trực giác nhạy bén, biết lắng nghe, bao dung và giàu tình cảm.", 
            "diem_yeu": "Quá nhạy cảm, dễ bị tổn thương, hay do dự, nhút nhát, và có xu hướng phụ thuộc, đánh mất ranh giới cá nhân." 
        },
        "3": { 
            "y_nghia_tong_quat": "Đường đời 3 là con đường của sự bộc lộ sáng tạo, giao tiếp và truyền cảm hứng. Bạn sinh ra để mang lại niềm vui, sự lạc quan và sử dụng ngôn từ/nghệ thuật để lan tỏa năng lượng tích cực.", 
            "diem_manh": "Hoạt ngôn, hài hước, sáng tạo nghệ thuật, lạc quan, thân thiện và có sức hút cá nhân mạnh mẽ.", 
            "diem_yeu": "Dễ phân tán năng lượng, cả thèm chóng chán, đôi khi hời hợt, bốc đồng và gặp khó khăn trong việc quản lý chi tiêu." 
        },
        "4": { 
            "y_nghia_tong_quat": "Đường đời 4 là con đường của sự thực tế, kỷ luật và kiến tạo nền tảng vững chắc. Bài học của bạn là hiểu được giá trị của sự kiên trì và làm việc có hệ thống để tạo ra những giá trị lâu bền.", 
            "diem_manh": "Chăm chỉ, thực tế, có đầu óc tổ chức cao, trung thành, kiên định và cực kỳ đáng tin cậy.", 
            "diem_yeu": "Cứng nhắc, bảo thủ, thiếu linh hoạt, dễ rơi vào trạng thái tham công tiếc việc, và đôi khi bi quan hoặc quá tiểu tiết." 
        },
        "5": { 
            "y_nghia_tong_quat": "Đường đời 5 là con đường của tự do, phiêu lưu và trải nghiệm đa dạng. Bạn khao khát phá vỡ giới hạn, khám phá thế giới và học hỏi thông qua việc thích nghi với những thay đổi liên tục.", 
            "diem_manh": "Linh hoạt, tháo vát, dũng cảm, thích nghi cực nhanh, giao tiếp giỏi và đầy tính hiếu kỳ, sáng tạo.", 
            "diem_yeu": "Dễ bốc đồng, thiếu kỷ luật, e ngại sự cam kết ràng buộc, và dễ sa đà vào các thói quen nuông chiều bản thân khi chán nản." 
        },
        "6": { 
            "y_nghia_tong_quat": "Đường đời 6 là con đường của trách nhiệm, tình yêu thương và sự nuôi dưỡng. Bài học trọng tâm của bạn là chăm sóc gia đình, cộng đồng, và duy trì sự cân bằng, hòa hợp trong môi trường sống.", 
            "diem_manh": "Bao dung, đáng tin cậy, giàu lòng trắc ẩn, có tinh thần trách nhiệm cực cao, yêu nghệ thuật và sự hoàn mỹ.", 
            "diem_yeu": "Hay lo bao đồng, có xu hướng kiểm soát hoặc can thiệp quá mức vì muốn 'tốt cho người khác', dễ tự ái và hay hy sinh thái quá dẫn đến oán giận." 
        },
        "7": { 
            "y_nghia_tong_quat": "Đường đời 7 là con đường của trí tuệ, sự tìm tòi chân lý và phát triển nội tâm. Trọng trách của bạn là đi sâu vào bản chất của vạn vật, phân tích sự thật và thấu hiểu các quy luật triết học, tâm linh.", 
            "diem_manh": "Trí tuệ sắc bén, trực giác sâu sắc, khả năng quan sát tinh tế, độc lập trong tư duy và giỏi phân tích, nghiên cứu.", 
            "diem_yeu": "Sống khép kín, đa nghi, khó gần, có xu hướng cô lập bản thân, đôi khi quá cầu toàn, lạnh lùng hoặc dễ bi quan." 
        },
        "8": { 
            "y_nghia_tong_quat": "Đường đời 8 là con đường của quyền lực, thành tựu vật chất và làm chủ tài chính. Bài học của bạn là cân bằng giữa thế giới vật chất và tinh thần, sử dụng quyền hạn để tạo ra lợi ích lớn lao.", 
            "diem_manh": "Có tầm nhìn vĩ mô, khả năng quản lý/kinh doanh xuất sắc, quyết đoán, thực tế, đầy tham vọng và bản lĩnh.", 
            "diem_yeu": "Có thể quá coi trọng vật chất, tham công tiếc việc, khao khát kiểm soát, đôi khi trở nên tàn nhẫn hoặc thiếu sự đồng cảm." 
        },
        "9": { 
            "y_nghia_tong_quat": "Đường đời 9 là con đường của lòng nhân đạo, sự buông bỏ và tình yêu thương phổ quát. Bạn mang trong mình lý tưởng cao đẹp, mong muốn cống hiến để làm cho thế giới trở nên tốt đẹp hơn.", 
            "diem_manh": "Giàu lòng vị tha, lý tưởng hóa, từ bi, sáng tạo, có tầm nhìn bao quát và vô cùng rộng lượng.", 
            "diem_yeu": "Dễ bị lợi dụng tình cảm, hay thất vọng đau khổ vì người khác không đạt được lý tưởng của mình, thiếu thực tế, đôi khi quá nhạy cảm." 
        },
        "11": { 
            "y_nghia_tong_quat": "Là con số 'Người soi đường', Đường đời 11 mang năng lượng của sự thức tỉnh tâm linh và nguồn cảm hứng. Bài học của bạn là sử dụng trực giác phi thường để dẫn dắt và mang lại ánh sáng nhận thức cho người khác.", 
            "diem_manh": "Trực giác cực kỳ nhạy bén, khả năng thấu cảm thâm sâu, sáng tạo vượt trội, có sức hút tâm linh và năng lực truyền cảm hứng mạnh mẽ.", 
            "diem_yeu": "Thường xuyên căng thẳng thần kinh, quá nhạy cảm với năng lượng môi trường xung quanh, đôi khi kỳ vọng thiếu thực tế hoặc mộng mơ xa rời thực tại." 
        },
        "22": { 
            "y_nghia_tong_quat": "Được mệnh danh là 'Bậc thầy kiến tạo' (Master Builder), Đường đời 22 kết hợp tầm nhìn lý tưởng của số 11 với tính thực tế của số 4. Bạn mang sứ mệnh hiện thực hóa những dự án quy mô lớn, tạo ra di sản lâu dài cho nhân loại.", 
            "diem_manh": "Năng lực tổ chức xuất chúng, tầm nhìn vĩ mô, khả năng lãnh đạo các dự án thực tiễn lớn, biến giấc mơ không tưởng thành hiện thực vật chất.", 
            "diem_yeu": "Tự tạo áp lực bản thân khổng lồ, sợ hãi thất bại, có xu hướng trở nên độc đoán, nếu tiêu cực có thể thao túng hoặc dùng quyền lực sai mục đích." 
        },
        "33": { 
            "y_nghia_tong_quat": "Là 'Bậc thầy chữa lành' (Master Teacher), Đường đời 33 mang năng lượng của tình yêu thương vô điều kiện và sự tận hiến cao cả. Bạn hướng tới việc nâng đỡ tinh thần, xoa dịu nỗi đau và chỉ dẫn cho cộng đồng.", 
            "diem_manh": "Trái tim bao la, lòng từ bi sâu sắc, khả năng chữa lành cảm xúc vô song, luôn sẵn sàng hy sinh vì lợi ích lớn, có sức ảnh hưởng tích cực lan tỏa.", 
            "diem_yeu": "Dễ gánh vác quá nhiều nỗi đau của người khác dẫn đến kiệt sức, có xu hướng tử vì đạo, bỏ bê nhu cầu thiết yếu của bản thân, dễ bị lợi dụng lòng tốt." 
        }
    },

    "su_menh": {
        "_description": "Destiny/Expression Number - Dựa trên tổng chữ cái của tên khai sinh (Sứ mệnh, tài năng và định hướng)",
        "1": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là trở thành người lãnh đạo, người tiên phong và tạo ra những lối đi mới. Bạn được trang bị năng lượng để hoàn thành những mục tiêu mang tính cá nhân và độc lập.", 
            "nang_khieu": "Tự chủ, sáng tạo độc lập, quản lý và dẫn dắt người khác, khả năng khởi xướng dự án mới.", 
            "dinh_huong_nghe_nghiep": "Giám đốc điều hành (CEO), doanh nhân khởi nghiệp, nhà phát minh, quản lý cấp cao, vận động viên độc lập." 
        },
        "2": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là trở thành người hòa giải, duy trì sự cân bằng và thúc đẩy sự hợp tác. Bạn mang lại sự thấu hiểu và hòa bình cho bất kỳ tập thể nào bạn tham gia.", 
            "nang_khieu": "Giao tiếp ngoại giao, thấu cảm, làm việc nhóm xuất sắc, giải quyết xung đột, tư vấn tâm lý.", 
            "dinh_huong_nghe_nghiep": "Cố vấn, nhà ngoại giao, thư ký, trợ lý cao cấp, người làm công tác xã hội, nghệ sĩ." 
        },
        "3": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là biểu đạt bản thân, truyền cảm hứng và mang lại niềm vui cho thế giới thông qua giao tiếp và nghệ thuật.", 
            "nang_khieu": "Khả năng ngôn ngữ ưu việt, hài hước, sáng tạo nghệ thuật, thu hút đám đông, diễn đạt truyền cảm.", 
            "dinh_huong_nghe_nghiep": "Diễn giả, nhà báo, diễn viên, ca sĩ, nghệ sĩ, nhà văn, chuyên viên marketing/PR." 
        },
        "4": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là kiến thiết nền tảng, thiết lập trật tự và tạo ra những kết quả thực tế, lâu bền cho bản thân và xã hội.", 
            "nang_khieu": "Tổ chức hệ thống, chú ý chi tiết, quản lý quy trình, kiên trì, làm việc kỷ luật.", 
            "dinh_huong_nghe_nghiep": "Kiến trúc sư, kỹ sư, kế toán, nhà thầu xây dựng, quản trị viên, người làm luật." 
        },
        "5": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là trải nghiệm tự do, lan tỏa sự năng động và thúc đẩy sự thay đổi tích cực trong môi trường xung quanh.", 
            "nang_khieu": "Thích nghi nhanh, nắm bắt xu hướng, giao tiếp đa văn hóa, ứng biến linh hoạt, bán hàng xuất sắc.", 
            "dinh_huong_nghe_nghiep": "Hướng dẫn viên du lịch, chuyên gia bán hàng, nhà truyền thông, phóng viên, người làm nghề tự do (freelancer)." 
        },
        "6": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là chăm sóc, giáo dục và mang lại sự chữa lành, bảo bọc cho gia đình cũng như cộng đồng.", 
            "nang_khieu": "Chăm sóc y tế/tâm lý, tư vấn gia đình, khiếu thẩm mỹ, khả năng tạo sự ấm cúng và an toàn.", 
            "dinh_huong_nghe_nghiep": "Bác sĩ, y tá, giáo viên, chuyên gia tâm lý, nhà thiết kế nội thất, quản lý nhân sự." 
        },
        "7": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là tìm kiếm chân lý, nghiên cứu chuyên sâu và giải mã những bí ẩn của tự nhiên, khoa học hoặc tâm linh.", 
            "nang_khieu": "Phân tích logic, quan sát sắc bén, tư duy triết học, năng lực nghiên cứu độc lập.", 
            "dinh_huong_nghe_nghiep": "Nhà khoa học, nhà nghiên cứu, lập trình viên, triết gia, nhà phân tích dữ liệu, học giả." 
        },
        "8": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là làm chủ thế giới vật chất, vận hành các nguồn lực tài chính lớn và thể hiện uy quyền một cách công bằng.", 
            "nang_khieu": "Nhạy bén tài chính, điều hành tổ chức lớn, tư duy chiến lược, khả năng thương thuyết.", 
            "dinh_huong_nghe_nghiep": "Chuyên gia tài chính, giám đốc ngân hàng, nhà đầu tư, chủ doanh nghiệp lớn, luật sư, thẩm phán." 
        },
        "9": { 
            "y_nghia_tong_quat": "Sứ mệnh của bạn là phụng sự nhân loại, nâng cao nhận thức cộng đồng và để lại những giá trị mang tính toàn cầu.", 
            "nang_khieu": "Tầm nhìn vị nhân sinh, sáng tạo nghệ thuật quy mô lớn, khả năng chữa lành và cảm hóa đám đông.", 
            "dinh_huong_nghe_nghiep": "Nhà hoạt động xã hội, nhà từ thiện, chính trị gia, nghệ sĩ truyền cảm hứng, nhà giáo dục cộng đồng." 
        },
        "11": { 
            "y_nghia_tong_quat": "Sứ mệnh Master của bạn là mang lại sự thức tỉnh tâm linh, đóng vai trò như một người dẫn đường tinh thần và cầu nối với thế giới siêu thực.", 
            "nang_khieu": "Trực giác ngoại cảm, thấu cảm sâu sắc, năng lực truyền cảm hứng tâm linh, sáng tạo đột phá.", 
            "dinh_huong_nghe_nghiep": "Nhà lãnh đạo tinh thần, cố vấn tâm lý học sâu, nghệ sĩ có tầm nhìn xa, nhà triết học, nhà chữa lành." 
        },
        "22": { 
            "y_nghia_tong_quat": "Sứ mệnh Master của bạn là biến những lý tưởng vĩ đại thành hiện thực vật chất, xây dựng những công trình để đời cho nhân loại.", 
            "nang_khieu": "Năng lực kiến tạo quy mô lớn, quản lý dự án vĩ mô, khả năng thực thi các ý tưởng không tưởng.", 
            "dinh_huong_nghe_nghiep": "Nhà hoạch định chiến lược quốc gia, kiến trúc sư trưởng, lãnh đạo các tập đoàn đa quốc gia, chính khách." 
        },
        "33": { 
            "y_nghia_tong_quat": "Sứ mệnh Master của bạn là tỏa ra tình yêu thương vô điều kiện, trở thành chỗ dựa tinh thần và chữa lành những tổn thương sâu sắc của xã hội.", 
            "nang_khieu": "Lòng từ bi vô hạn, khả năng chữa lành cảm xúc, đức hy sinh, sức mạnh lan tỏa tình yêu thương.", 
            "dinh_huong_nghe_nghiep": "Nhà giáo dục vĩ đại, bác sĩ nhân đạo, nhà lãnh đạo tôn giáo/tâm linh, người thành lập các quỹ từ thiện lớn." 
        }
    },

    "linh_hon": {
        "_description": "Soul Urge Number - Dựa trên tổng các nguyên âm trong tên khai sinh (Khát khao và động lực ẩn sâu bên trong)",
        "1": { 
            "khao_khat_ben_trong": "Bạn khao khát mãnh liệt được độc lập, tự do làm theo ý mình, được tôn trọng như một người dẫn đầu và không phải phụ thuộc vào ai.", 
            "dong_luc_noi_tam": "Sự tự chủ, quyền quyết định cá nhân và mong muốn để lại dấu ấn riêng biệt." 
        },
        "2": { 
            "khao_khat_ben_trong": "Bạn khao khát một môi trường hòa hợp, tình yêu thương, sự sẻ chia và mong muốn cảm thấy mình được thuộc về một ai đó hoặc một tập thể.", 
            "dong_luc_noi_tam": "Tình yêu, sự thấu hiểu đồng điệu và một cuộc sống bình yên không có xung đột." 
        },
        "3": { 
            "khao_khat_ben_trong": "Bạn khao khát được bộc lộ bản thân, được tỏa sáng, mang lại niềm vui cho người khác và được mọi người chú ý, công nhận tài năng.", 
            "dong_luc_noi_tam": "Niềm vui sống, sự sáng tạo nghệ thuật và sự kết nối vui vẻ với xã hội." 
        },
        "4": { 
            "khao_khat_ben_trong": "Bạn khao khát một cuộc sống có trật tự, ổn định, an toàn. Bạn muốn xây dựng những thứ bền vững và kiểm soát được môi trường xung quanh.", 
            "dong_luc_noi_tam": "Sự an tâm về nền tảng vật chất, sự chắc chắn và kết quả thực tế có thể nhìn thấy." 
        },
        "5": { 
            "khao_khat_ben_trong": "Bạn khao khát sự tự do tuyệt đối, những chuyến phiêu lưu, sự thay đổi không ngừng và những trải nghiệm kích thích giác quan.", 
            "dong_luc_noi_tam": "Sự tò mò, khám phá cái mới và thoát khỏi những lề thói nhàm chán hàng ngày." 
        },
        "6": { 
            "khao_khat_ben_trong": "Bạn khao khát có một gia đình hạnh phúc, được chăm sóc và bảo bọc những người thân yêu, tạo ra một không gian ấm cúng, hài hòa.", 
            "dong_luc_noi_tam": "Tình yêu thương gia đình, sự phụng sự người thân và nhu cầu được cần đến." 
        },
        "7": { 
            "khao_khat_ben_trong": "Bạn khao khát sự thật, trí tuệ sâu sắc và không gian tĩnh lặng để chiêm nghiệm, thấu hiểu những quy luật ẩn giấu của vũ trụ.", 
            "dong_luc_noi_tam": "Kiến thức tâm linh/triết học, sự bình an nội tâm và nhu cầu tìm ra câu trả lời cho các câu hỏi lớn." 
        },
        "8": { 
            "khao_khat_ben_trong": "Bạn khao khát thành công, quyền lực, sự giàu có và được công nhận rộng rãi về địa vị xã hội cũng như năng lực tài chính.", 
            "dong_luc_noi_tam": "Sự tự chủ kinh tế, thành tựu vật chất và khả năng kiểm soát số phận của mình." 
        },
        "9": { 
            "khao_khat_ben_trong": "Bạn khao khát một thế giới hoàn mỹ, nơi mọi người yêu thương nhau. Bạn muốn cống hiến hết mình để giảm bớt sự đau khổ của nhân loại.", 
            "dong_luc_noi_tam": "Lý tưởng nhân đạo, tình yêu thương vô biên và khao khát phụng sự cộng đồng." 
        },
        "11": { 
            "khao_khat_ben_trong": "Bạn khao khát đạt tới sự giác ngộ, thức tỉnh tâm linh và muốn truyền đạt những chân lý siêu việt ấy để soi sáng cho người khác.", 
            "dong_luc_noi_tam": "Sự kết nối trực giác với vũ trụ và nhu cầu mang lại ánh sáng tinh thần cho đời sống." 
        },
        "22": { 
            "khao_khat_ben_trong": "Bạn khao khát để lại những di sản vĩ đại, những công trình kiến tạo mang tính lịch sử có thể thay đổi cách vận hành của cả xã hội.", 
            "dong_luc_noi_tam": "Tầm nhìn vĩ mô, khát vọng biến những lý tưởng to lớn thành hiện thực bền vững." 
        },
        "33": { 
            "khao_khat_ben_trong": "Bạn khao khát trở thành bến đỗ bình yên cho những linh hồn tổn thương, sẵn sàng hy sinh lợi ích cá nhân vì tình yêu thương vô điều kiện.", 
            "dong_luc_noi_tam": "Lòng từ bi tối thượng và khát vọng chữa lành toàn diện cho mọi người xung quanh." 
        }
    },

    "nhan_cach": {
        "_description": "Personality Number - Dựa trên tổng các phụ âm trong tên khai sinh (Lăng kính bên ngoài, ấn tượng ban đầu)",
        "1": { 
            "an_tuong_ben_ngoai": "Tự tin, độc lập, uy quyền và toát ra phong thái của một người dẫn đầu. Bạn có vẻ ngoài mạnh mẽ và quyết đoán.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn là người có năng lực, dứt khoát nhưng đôi khi có vẻ lạnh lùng, xa cách, khó gần hoặc hơi tự mãn." 
        },
        "2": { 
            "an_tuong_ben_ngoai": "Hòa nhã, thân thiện, dễ gần, có phong thái từ tốn và biết lắng nghe. Trang phục thường nền nã, lịch sự.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn là một người bạn đáng tin cậy, nhẹ nhàng, nhưng đôi lúc có vẻ nhút nhát, thiếu quyết đoán hoặc quá thụ động." 
        },
        "3": { 
            "an_tuong_ben_ngoai": "Cuốn hút, tươi sáng, vui vẻ, thường có gu thời trang nổi bật hoặc rực rỡ. Bạn tỏa ra năng lượng tích cực, dễ mến.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất duyên dáng, thú vị, là trung tâm của bữa tiệc, nhưng đôi khi có vẻ phù phiếm hoặc thiều chiều sâu." 
        },
        "4": { 
            "an_tuong_ben_ngoai": "Nghiêm túc, đứng đắn, chỉnh chu. Phong cách ăn mặc gọn gàng, thực dụng và không phô trương.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất đáng tin cậy, làm việc chăm chỉ, nguyên tắc, nhưng thỉnh thoảng bị đánh giá là cứng nhắc, bảo thủ hoặc tẻ nhạt." 
        },
        "5": { 
            "an_tuong_ben_ngoai": "Năng động, nhanh nhẹn, hoạt bát, toát lên sự phóng khoáng và hiện đại. Ánh mắt thường lanh lợi và tò mò.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất linh hoạt, thú vị, đầy sức sống, nhưng đôi khi tạo cảm giác bốc đồng, khó nắm bắt hoặc không đáng tin cậy." 
        },
        "6": { 
            "an_tuong_ben_ngoai": "Ấm áp, ân cần, ra dáng 'người cha/người mẹ' chăm sóc. Phong thái tạo sự an tâm, thân thuộc và có tính thẩm mỹ cao.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất trách nhiệm, đáng tin cậy, thích bao bọc, nhưng nhiều khi có vẻ quá lo toan, can thiệp sâu hoặc hay cằn nhằn." 
        },
        "7": { 
            "an_tuong_ben_ngoai": "Trí thức, bí ẩn, tĩnh lặng, ánh mắt sâu thẳm mang tính quan sát. Có phong thái đĩnh đạc và hơi tách biệt.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất sâu sắc, thông thái, nhưng thường mang lại cảm giác xa cách, khó hiểu, khép kín hoặc lạnh lùng." 
        },
        "8": { 
            "an_tuong_ben_ngoai": "Quyền lực, sang trọng, toát lên tố chất của một doanh nhân thành đạt. Phong thái tự tin, mạnh mẽ và kiểm soát.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất bản lĩnh, có uy tín, giỏi giang, nhưng dễ tạo cảm giác áp đảo, tham vọng quá mức hoặc hách dịch." 
        },
        "9": { 
            "an_tuong_ben_ngoai": "Rộng lượng, quý phái, bao dung, có vẻ đẹp lý tưởng hóa. Phong thái điềm đạm mang tính nghệ sĩ hoặc nhà tư tưởng.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất nhân hậu, đáng kính, hào hiệp, nhưng thỉnh thoảng có vẻ như đang sống ở một thế giới khác, xa rời thực tại." 
        },
        "11": { 
            "an_tuong_ben_ngoai": "Đặc biệt, toát ra khí chất thanh tao, vô cùng nhạy cảm. Thường có ánh nhìn xa xăm, mơ màng.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn rất tâm linh, tinh tế, đầy cảm hứng, nhưng đôi lúc có vẻ quá mộng mơ, lập dị hoặc mong manh dễ vỡ." 
        },
        "22": { 
            "an_tuong_ben_ngoai": "Cực kỳ bản lĩnh, vững chãi, uy nghi. Toát ra trường năng lượng khiến người khác cảm thấy bạn có thể giải quyết mọi việc.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn là một nhà tổ chức vĩ đại, đáng nể trọng, uy quyền, nhưng có thể hơi độc đoán hoặc tạo áp lực vô hình lên người đối diện." 
        },
        "33": { 
            "an_tuong_ben_ngoai": "Vô cùng nhân hậu, tỏa ra năng lượng an bình, ánh mắt chan chứa từ bi khiến ai cũng muốn tìm đến để giãi bày.", 
            "cach_nguoi_khac_nhin_nhan": "Họ thấy bạn như một bậc thánh nhân đầy lòng trắc ẩn, hy sinh, nhưng đôi khi có cảm giác bạn tự gánh quá nhiều khổ đau của thế gian." 
        }
    }
}

with open(r'd:\All Code\New folder\Numerology_Project\data\than_so_hoc_bang_tra_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Updated JSON file with 48 fully detailed nodes!")
