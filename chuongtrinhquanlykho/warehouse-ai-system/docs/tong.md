# Tổng hợp doanh nghiệp thu mua giả định

## Phạm vi

Tài liệu này mô phỏng 10 doanh nghiệp có nhu cầu thu mua các mặt hàng đang tồn tại trong hệ thống. Dữ liệu chỉ phục vụ phân tích, demo và xây dựng kịch bản nghiệp vụ; **không tự động tạo nhà cung cấp, đơn đặt hàng hoặc giao dịch trong database**.

Mức giá trong tài liệu được tính theo giá bán tham chiếu hiện có của hàng hóa trong `database/seed_data.sql`:

```text
Giá đề xuất = Giá tham chiếu x (1 + Mức điều chỉnh)
```

- Mức thấp nhất: `-50%` giá tham chiếu.
- Mức cao nhất: `+100%` giá tham chiếu.
- Đơn vị tiền tệ: VND.
- Các mức giá là giá giả định theo từng tình huống thu mua, không phải giá giao dịch thực tế.

## Mặt hàng và giá tham chiếu

| SKU | Mặt hàng | Đơn vị | Giá tham chiếu |
|---|---|---:|---:|
| NL001 | Hạt nhựa PP nguyên sinh | Kg | 42.000 |
| NL002 | Phụ gia chống UV cho nhựa | Kg | 68.000 |
| NL003 | Thép cuộn cán nguội | Kg | 26.500 |
| NL004 | Nhôm tấm 2mm | Tấm | 185.000 |
| NL005 | Dung môi công nghiệp IPA | Can | 95.000 |
| NL006 | Chất đóng rắn epoxy | Kg | 145.000 |
| BTP001 | Cụm mạch điều khiển nguồn | Bộ | 320.000 |
| BTP002 | Module hiển thị LCD 16x2 | Bộ | 98.000 |
| BTP003 | Khung thép sơn tĩnh điện | Cái | 285.000 |
| BTP004 | Vỏ nhôm gia công CNC | Cái | 410.000 |
| TP001 | Bộ điều khiển đóng gói hoàn chỉnh | Bộ | 1.250.000 |
| TP002 | Thiết bị giám sát nhiệt độ | Cái | 890.000 |

## Danh sách doanh nghiệp giả định

### 1. Công ty TNHH Bao Bì Xanh Việt

Mặt hàng quan tâm: **NL001 - Hạt nhựa PP nguyên sinh**. Giá tham chiếu: **42.000 VND/Kg**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Đặt số lượng lớn theo hợp đồng quý | -20% | 33.600 |
| 2 | Thanh toán ngay trong ngày | -10% | 37.800 |
| 3 | Nhận hàng tại kho bên bán, giảm chi phí vận chuyển | -15% | 35.700 |
| 4 | Cần giao gấp trong 24 giờ | +25% | 52.500 |
| 5 | Hạt nhựa đạt chứng nhận an toàn bao bì thực phẩm | +40% | 58.800 |
| 6 | Nhu cầu tăng đột biến trước mùa cao điểm đóng gói | +60% | 67.200 |

### 2. Công ty CP Cơ Khí Đại Thành

Mặt hàng quan tâm: **NL003 - Thép cuộn cán nguội**. Giá tham chiếu: **26.500 VND/Kg**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua theo lô lớn và nhận hàng nhiều đợt | -25% | 19.875 |
| 2 | Thép có bề mặt tiêu chuẩn, ít lỗi gia công | +15% | 30.475 |
| 3 | Yêu cầu cắt cuộn theo kích thước riêng | +30% | 34.450 |
| 4 | Nguồn thép khan hiếm trong thời gian ngắn | +50% | 39.750 |
| 5 | Cần giao hỏa tốc cho dự án đang trễ tiến độ | +75% | 46.375 |
| 6 | Đơn hàng có yêu cầu kiểm định vật liệu độc lập | +100% | 53.000 |

### 3. Công ty TNHH Thiết Bị Nhiệt Lạnh An Phát

Mặt hàng quan tâm: **TP002 - Thiết bị giám sát nhiệt độ**. Giá tham chiếu: **890.000 VND/Cái**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua số lượng nhỏ để chạy thử hệ thống | +10% | 979.000 |
| 2 | Yêu cầu cấu hình và hiệu chuẩn theo kho lạnh | +35% | 1.201.500 |
| 3 | Cần giao trong ngày tại công trường xa | +50% | 1.335.000 |
| 4 | Sản phẩm có đầy đủ hồ sơ bảo hành mở rộng | +65% | 1.468.500 |
| 5 | Thiếu thiết bị thay thế trên thị trường | +80% | 1.602.000 |
| 6 | Đơn hàng khẩn cấp để xử lý sự cố dây chuyền | +100% | 1.780.000 |

### 4. Công ty CP Điện Tử Minh Quang

Mặt hàng quan tâm: **BTP001 - Cụm mạch điều khiển nguồn**. Giá tham chiếu: **320.000 VND/Bộ**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua theo mẫu để đánh giá tương thích | -30% | 224.000 |
| 2 | Đặt lại số lượng lớn theo kế hoạch sản xuất | -20% | 256.000 |
| 3 | Yêu cầu test 100% trước khi giao | +25% | 400.000 |
| 4 | Cần đóng gói chống tĩnh điện riêng | +35% | 432.000 |
| 5 | Đặt hàng ngoài lịch sản xuất thông thường | +55% | 496.000 |
| 6 | Cần thay thế khẩn cấp cho lô hàng lỗi | +90% | 608.000 |

### 5. Công ty TNHH Nội Thất Kim Loại Việt

Mặt hàng quan tâm: **NL004 - Nhôm tấm 2mm**. Giá tham chiếu: **185.000 VND/Tấm**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Nhận nhôm có vết xước nhẹ để gia công lại | -40% | 111.000 |
| 2 | Mua theo lô tồn kho lâu ngày | -25% | 138.750 |
| 3 | Yêu cầu bề mặt đẹp cho sản phẩm trưng bày | +20% | 222.000 |
| 4 | Cần cắt phôi theo bản vẽ riêng | +40% | 259.000 |
| 5 | Yêu cầu giao từng tấm có màng bảo vệ | +60% | 296.000 |
| 6 | Cần đủ vật liệu cho đơn hàng khai trương gấp | +85% | 342.250 |

### 6. Công ty CP Sơn Và Vật Liệu Phủ Nam Việt

Mặt hàng quan tâm: **NL006 - Chất đóng rắn epoxy**. Giá tham chiếu: **145.000 VND/Kg**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua gần ngày hết hạn nhưng vẫn đạt kiểm nghiệm | -50% | 72.500 |
| 2 | Nhận hàng bao bì ngoài tiêu chuẩn | -30% | 101.500 |
| 3 | Yêu cầu kiểm tra độ tinh khiết theo lô | +30% | 188.500 |
| 4 | Cần bảo quản và vận chuyển theo điều kiện đặc biệt | +50% | 217.500 |
| 5 | Đặt ngoài kế hoạch do khách hàng đổi công thức | +70% | 246.500 |
| 6 | Mua gấp để khắc phục thiếu nguyên liệu sản xuất | +100% | 290.000 |

### 7. Công ty TNHH Giải Pháp Hiển Thị Sao Việt

Mặt hàng quan tâm: **BTP002 - Module hiển thị LCD 16x2**. Giá tham chiếu: **98.000 VND/Bộ**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua số lượng nhỏ cho dự án thử nghiệm | +15% | 112.700 |
| 2 | Đặt theo lô tiêu chuẩn, không cần tùy biến | -15% | 83.300 |
| 3 | Yêu cầu kiểm tra điểm ảnh trước khi giao | +25% | 122.500 |
| 4 | Cần giao nhanh cùng bộ cáp kết nối | +45% | 142.100 |
| 5 | Nhu cầu tăng do mở rộng dây chuyền | +65% | 161.700 |
| 6 | Khan hiếm linh kiện tương thích trong nước | +90% | 186.200 |

### 8. Công ty CP Gia Công Vỏ Thiết Bị Bắc Nam

Mặt hàng quan tâm: **BTP004 - Vỏ nhôm gia công CNC**. Giá tham chiếu: **410.000 VND/Cái**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua lô có sai lệch màu nhỏ để sơn lại | -35% | 266.500 |
| 2 | Đặt hàng theo bản vẽ có sẵn | -10% | 369.000 |
| 3 | Yêu cầu gia công thêm lỗ và ren | +30% | 533.000 |
| 4 | Cần kiểm tra kích thước bằng máy đo 3D | +45% | 594.500 |
| 5 | Giao gấp cho dây chuyền lắp ráp | +70% | 697.000 |
| 6 | Mẫu mã độc quyền cần giữ khuôn và bảo mật | +100% | 820.000 |

### 9. Công ty TNHH Tự Động Hóa Đông Dương

Mặt hàng quan tâm: **BTP003 - Khung thép sơn tĩnh điện**. Giá tham chiếu: **285.000 VND/Cái**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua theo lô thanh lý còn đạt tiêu chuẩn kỹ thuật | -45% | 156.750 |
| 2 | Nhận khung chưa đóng gói hoàn thiện | -20% | 228.000 |
| 3 | Yêu cầu màu sơn riêng theo nhận diện thương hiệu | +25% | 356.250 |
| 4 | Cần bổ sung lớp sơn chống ăn mòn | +40% | 399.000 |
| 5 | Đặt gấp cho dự án lắp đặt nhà máy | +65% | 470.250 |
| 6 | Yêu cầu giao ngoài giờ và lắp thử tại hiện trường | +85% | 527.250 |

### 10. Công ty CP Thiết Bị Điều Khiển Thành Công

Mặt hàng quan tâm: **TP001 - Bộ điều khiển đóng gói hoàn chỉnh**. Giá tham chiếu: **1.250.000 VND/Bộ**.

| STT | Lý do thu mua | Điều chỉnh | Giá giả định |
|---:|---|---:|---:|
| 1 | Mua số lượng lớn theo hợp đồng năm | -30% | 875.000 |
| 2 | Thanh toán trước toàn bộ đơn hàng | -20% | 1.000.000 |
| 3 | Yêu cầu tích hợp thêm phần mềm điều khiển | +35% | 1.687.500 |
| 4 | Cần chứng nhận kiểm thử và truy xuất từng bộ | +50% | 1.875.000 |
| 5 | Giao hàng khẩn cấp để thay thế thiết bị hỏng | +75% | 2.187.500 |
| 6 | Đơn hàng đặc biệt kèm đào tạo vận hành tại chỗ | +100% | 2.500.000 |

## Quy tắc sử dụng dữ liệu mô phỏng

1. Đây là các doanh nghiệp **thu mua giả định**, không phải nhà cung cấp đã có trong seed dữ liệu.
2. Giá tham chiếu là giá bán hiện có của hàng hóa; khi lập giao dịch thật cần dùng giá thực tế theo hợp đồng.
3. Mức điều chỉnh âm không thấp hơn `-50%` và mức điều chỉnh dương không cao hơn `+100%`.
4. Giá mua cao hơn có thể do giao gấp, tùy biến, kiểm định, bảo hành hoặc dịch vụ đi kèm.
5. Giá mua thấp hơn có thể do mua số lượng lớn, thanh toán sớm, nhận hàng tại kho hoặc chấp nhận hàng cần xử lý thêm.
6. Khi đưa dữ liệu vào hệ thống thật, cần tạo doanh nghiệp ở module phù hợp rồi mới lập đơn hàng hoặc phiếu giao dịch.

## Kịch bản giá bán của nhà cung cấp hiện có

Phần này mô phỏng trường hợp 6 nhà cung cấp đang có trong seed dữ liệu báo giá
cho doanh nghiệp. Mỗi nhà cung cấp có 6 lý do định giá khác nhau. Giá bán được
tính theo giá tham chiếu của mặt hàng:

```text
Giá bán giả định = Giá tham chiếu x (1 + Mức điều chỉnh)
```

- Giá thấp nhất được phép là `75%` giá tham chiếu, tương đương giảm tối đa `25%`.
- Giá cao nhất được phép là `150%` giá tham chiếu, tương đương tăng tối đa `50%`.
- Một số lý do được lặp lại có chủ đích để phản ánh tình huống kinh doanh thực tế.

### 1. Công ty TNHH Nguyên Liệu Nhựa Việt

Mặt hàng báo giá: **NL001 - Hạt nhựa PP nguyên sinh**. Giá tham chiếu: **42.000 VND/Kg**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Khách đặt số lượng lớn theo hợp đồng dài hạn | -25% | 31.500 |
| 2 | Khách thanh toán trước thời hạn | -15% | 35.700 |
| 3 | Hạt nhựa có chứng nhận nguồn gốc và chất lượng | +20% | 50.400 |
| 4 | Giá nguyên liệu đầu vào trên thị trường tăng | +30% | 54.600 |
| 5 | Yêu cầu giao hàng trong 24 giờ | +40% | 58.800 |
| 6 | Lô hàng cần đóng gói chống ẩm riêng | +50% | 63.000 |

### 2. Công ty CP Kim Loại Công Nghiệp Đông Nam

Mặt hàng báo giá: **NL004 - Nhôm tấm 2mm**. Giá tham chiếu: **185.000 VND/Tấm**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Đơn hàng số lượng lớn, giao theo lịch cố định | -20% | 148.000 |
| 2 | Khách nhận hàng trực tiếp tại kho nhà cung cấp | -10% | 166.500 |
| 3 | Nhôm có bề mặt tuyển chọn, ít sai xước | +15% | 212.750 |
| 4 | Cắt tấm theo kích thước riêng của khách | +25% | 231.250 |
| 5 | Giá phôi nhôm nhập khẩu biến động tăng | +35% | 249.750 |
| 6 | Đơn hàng cần giao gấp ngoài lịch xe | +50% | 277.500 |

### 3. Công ty TNHH Hóa Chất Sản Xuất Minh Phát

Mặt hàng báo giá: **NL006 - Chất đóng rắn epoxy**. Giá tham chiếu: **145.000 VND/Kg**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Khách mua trọn lô còn thời hạn sử dụng phù hợp | -25% | 108.750 |
| 2 | Bao bì tiêu chuẩn, không yêu cầu chia nhỏ | -10% | 130.500 |
| 3 | Cần kiểm nghiệm độ tinh khiết theo từng lô | +20% | 174.000 |
| 4 | Hàng phải bảo quản và vận chuyển có kiểm soát | +30% | 188.500 |
| 5 | Khách yêu cầu giao gấp để không dừng dây chuyền | +40% | 203.000 |
| 6 | Lô hàng có hồ sơ an toàn hóa chất đầy đủ | +50% | 217.500 |

### 4. Công ty TNHH Linh Kiện Bán Thành Phẩm Á Châu

Mặt hàng báo giá: **BTP001 - Cụm mạch điều khiển nguồn**. Giá tham chiếu: **320.000 VND/Bộ**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Đặt mua theo lô tiêu chuẩn của nhà máy | -20% | 256.000 |
| 2 | Khách tự bố trí vận chuyển và nhận tại kho | -15% | 272.000 |
| 3 | Mạch được kiểm tra chức năng 100% trước khi giao | +20% | 384.000 |
| 4 | Yêu cầu đóng gói chống tĩnh điện riêng | +30% | 416.000 |
| 5 | Cần truy xuất số seri cho từng cụm mạch | +40% | 448.000 |
| 6 | Đơn hàng khẩn cấp thay thế lô bị lỗi | +50% | 480.000 |

### 5. Công ty CP Cơ Khí Bán Thành Phẩm Việt Thành

Mặt hàng báo giá: **BTP004 - Vỏ nhôm gia công CNC**. Giá tham chiếu: **410.000 VND/Cái**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Khách đặt số lượng lớn theo bản vẽ có sẵn | -25% | 307.500 |
| 2 | Khách chấp nhận thời gian giao hàng tiêu chuẩn | -10% | 369.000 |
| 3 | Gia công thêm lỗ, ren và xử lý bề mặt | +25% | 512.500 |
| 4 | Yêu cầu kiểm tra kích thước bằng máy đo 3D | +35% | 553.500 |
| 5 | Đơn hàng cần giao ngoài giờ làm việc | +40% | 574.000 |
| 6 | Khuôn gia công riêng chỉ phục vụ một khách hàng | +50% | 615.000 |

### 6. Công ty TNHH Sản Phẩm Hoàn Thiện Thành Công

Mặt hàng báo giá: **TP001 - Bộ điều khiển đóng gói hoàn chỉnh**. Giá tham chiếu: **1.250.000 VND/Bộ**.

| STT | Lý do bán hàng | Điều chỉnh | Giá bán giả định |
|---:|---|---:|---:|
| 1 | Khách ký hợp đồng mua định kỳ cả năm | -25% | 937.500 |
| 2 | Khách thanh toán trước toàn bộ đơn hàng | -15% | 1.062.500 |
| 3 | Bộ sản phẩm có gói bảo hành mở rộng | +20% | 1.500.000 |
| 4 | Yêu cầu kiểm thử và lập hồ sơ riêng từng bộ | +30% | 1.625.000 |
| 5 | Cần giao nhanh để thay thế thiết bị dừng hoạt động | +40% | 1.750.000 |
| 6 | Bao gồm đào tạo vận hành và hỗ trợ lắp đặt tại chỗ | +50% | 1.875.000 |

### Quy tắc sử dụng kịch bản nhà cung cấp

1. Sáu nhà cung cấp trong phần này là các nhà cung cấp hiện có trong `seed_data.sql`.
2. Mỗi nhà cung cấp có 6 lý do báo giá, trong đó một số lý do như mua số lượng lớn, thanh toán sớm hoặc giao gấp được phép xuất hiện lại ở nhà cung cấp khác.
3. Không có giá nào thấp hơn `75%` hoặc cao hơn `150%` giá tham chiếu.
4. Giá bán giả định không tự động thay đổi giá trong bảng hàng hóa; khi lập phiếu nhập, giá thực tế được lưu theo từng dòng phiếu nhập.
5. Các mặt hàng còn lại của từng nhà cung cấp có thể áp dụng cùng nhóm lý do, nhưng cần tính lại theo đúng giá tham chiếu và đơn vị tính.
