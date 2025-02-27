import requests
import json
import time
import pandas as pd
from tqdm import tqdm
import re
import unicodedata

url = "https://text.pollinations.ai/openai"


# def normalized(text):
#     return str(text).lower().strip().replace("-", " ").replace("_", " ").replace("[", " ").replace("]", " ")

lst_vo_nghia = [ "freeship", "trả góp","lắp đặt toàn quốc", "miễn phí vận chuyển", "ưu đãi hấp dẫn", "giao hàng nhanh", "mua ngay kẻo hết", "giảm giá sốc", "khuyến mãi lớn", "sản phẩm chất lượng", "giá cực kỳ rẻ", "mua ngay hôm nay", "ưu đãi cho bạn", "bảo hành chính hãng", "chất lượng đảm bảo", "giảm giá hôm nay", "hàng mới về", "giảm giá khủng", "sản phẩm bán chạy", "ưu đãi cực lớn", "giao hàng tận nơi", "sản phẩm hot nhất", "khuyến mãi đặc biệt", "giảm giá cực mạnh", "ưu đãi giảm giá", "chính hãng giá tốt", "mua nhiều giảm giá", "khuyến mãi cực lớn", "hàng về liên tục", "giá rẻ nhất", "giảm giá tận nơi", "chương trình khuyến mãi", "ưu đãi khách hàng", "siêu khuyến mãi", "đặt hàng ngay", "giảm ngay hôm nay", "giá siêu rẻ", "ưu đãi không giới hạn", "bảo đảm chất lượng", "chất lượng tốt nhất", "ưu đãi hấp dẫn", "giao hàng miễn phí", "chương trình ưu đãi", "bán chạy nhất", "giảm giá shock", "mua ngay giá rẻ", "khuyến mại hấp dẫn", "hàng chính hãng", "giảm giá cực khủng", "siêu giảm giá", "deal khủng hôm nay", "ưu đãi không giới hạn", "giảm giá lên đến", "mua 1 tặng 1", "ưu đãi duy nhất", "khuyến mãi bất ngờ", "hàng sale khủng", "sản phẩm hot trend", "giao hàng siêu nhanh", "giảm giá cực rẻ", "giảm giá hôm nay", "khuyến mãi giờ vàng", "ưu đãi đặc biệt", "khuyến mãi hôm nay", "sản phẩm chính hãng", "giảm giá hot nhất", "ưu đãi khách hàng", "bảo đảm uy tín", "hàng sale off", "giá rẻ bất ngờ", "khuyến mãi hôm nay", "mua sắm thông minh", "sản phẩm được yêu thích", "giảm giá cho bạn", "ưu đãi hấp dẫn", "mua hàng giá rẻ", "chất lượng hàng đầu", "bảo hành đổi trả", "hàng tồn kho", "hàng nhập khẩu", "ưu đãi đặc biệt", "giao hàng nhanh chóng", "giá ưu đãi hôm nay", "ưu đãi bất ngờ", "giảm giá đặc biệt", "mua liền tay", "chính hãng giá rẻ", "ưu đãi cuối tuần", "siêu phẩm hôm nay", "giá cực mềm", "săn deal giá rẻ", "hàng chính hãng", "bán chạy nhất", "hàng khuyến mãi", "giảm giá độc quyền", "hàng chất lượng cao", "siêu giảm giá", "chương trình đặc biệt", "deal cực lớn", "giảm mạnh hôm nay", "mua hàng ngay", "khuyến mãi hấp dẫn", "bán chạy nhất thị trường", "ưu đãi tốt nhất", "ưu đãi khách hàng", "giảm giá hôm nay", "sản phẩm mới về", "khuyến mãi siêu lớn", "giá sốc hôm nay", "mua ngay giảm giá", "giao hàng nhanh chóng", "siêu phẩm giảm giá", "giảm giá không giới hạn", "bán chạy nhất hôm nay", "deal hot hôm nay", "giảm giá sốc nhất", "giao hàng siêu tốc", "sản phẩm hot nhất", "ưu đãi lớn nhất", "bán giá siêu rẻ", "hàng về hôm nay", "siêu phẩm giảm mạnh", "giảm giá bất ngờ", "mua hàng ngay hôm nay", "giá ưu đãi nhất", "giảm giá chớp nhoáng", "giảm giá kịch sàn", "chương trình khuyến mãi lớn", "giảm giá kỷ lục", "mua nhanh kẻo hết", "giảm giá giờ vàng", "hàng về liên tục", "sản phẩm siêu hot", "giảm giá khủng nhất", "hàng về ngay hôm nay", "deal sốc hôm nay", "hàng giảm giá sâu", "giảm giá cực lớn", "deal cực kỳ hời", "khuyến mãi không thể bỏ lỡ", "sản phẩm giá rẻ", "hàng siêu giảm giá", "ưu đãi không thể bỏ qua", "giao hàng trong ngày", "giảm giá ngay hôm nay", "sản phẩm bán chạy nhất", "mua ngay không chần chừ", "giảm giá trong giờ vàng", "hàng về hôm nay", "ưu đãi đặc biệt hôm nay", "deal siêu hot", "khuyến mãi cuối tuần", "giảm giá nhanh chóng", "hàng giảm giá sốc", "mua liền không chần chừ", "ưu đãi duy nhất hôm nay", "giao hàng toàn quốc", "sản phẩm giảm giá", "siêu phẩm giá rẻ", "deal khủng nhất", "ưu đãi hôm nay", "khuyến mãi ngay hôm nay", "giảm giá hôm nay", "hàng về giá rẻ", "chương trình ưu đãi đặc biệt", "giảm giá hàng loạt", "giá rẻ tận gốc", "giảm giá không tưởng", "bán với giá rẻ", "khuyến mãi sốc hôm nay", "hàng khuyến mãi đặc biệt", "sản phẩm cực hot", "ưu đãi cuối cùng", "giảm giá cực mạnh hôm nay", "deal khủng nhất hôm nay", "giảm giá siêu mạnh", "giá sốc hôm nay", "sản phẩm mới về hôm nay", "hàng tồn giá rẻ", "mua ngay với giá rẻ", "hàng mới giảm giá", "bán giá ưu đãi", "giảm giá cực rẻ hôm nay", "deal cực lớn hôm nay", "bán chạy nhất hiện nay", "giảm giá cực khủng hôm nay", "sản phẩm tốt nhất", "mua hàng chất lượng", "giá cực kỳ ưu đãi", "giảm giá cực mạnh", "hàng thật", "hàng mới về", "hàng chính hãng", "hàng xách tay", "hàng nhập khẩu", "hàng đẹp", "hàng sale", "hàng giảm giá", "hàng sale off", "chính hãng", "nhập khẩu", "miễn phí", "khuyến mãi", "ưu đãi", "bán chạy", "giảm ngay", "sản phẩm hot", "bảo hành", "hàng chất lượng cao", "mới về", "mẫu mới", "giảm giá sốc", "mua ngay", "giá rẻ", "giao hàng nhanh", "giá ưu đãi", "deal hot", "đặt hàng ngay", "sản phẩm nổi bật", "giá tốt", "giảm sốc", "khuyến mại lớn", "giao hàng miễn phí", "số lượng có hạn", "hot deal", "siêu giảm giá", "mua sắm ngay", "bán lẻ", "chỉ còn hôm nay", "giao hàng trong ngày", "giảm cực mạnh", "hàng thanh lý", "siêu tiết kiệm", "giá cực rẻ", "hàng tồn kho", "mua liền tay", "ưu đãi khủng", "ưu đãi đặc biệt", "khuyến mãi lớn", "giảm giá kịch sàn", "đợt giảm giá", "chương trình khuyến mãi", "bảo đảm chất lượng", "đổi trả dễ dàng", "ưu đãi hấp dẫn", "xả kho", "hàng tồn", "thanh lý giá rẻ", "giảm giá mạnh", "giao hàng tận nơi", "quà tặng kèm", "giá sốc", "đặc biệt hôm nay", "giá siêu rẻ", "ưu đãi cuối tuần", "khuyến mãi hôm nay", "mua ngay kẻo hết", "mở bán giới hạn", "chỉ còn vài ngày", "giảm giá sâu", "sản phẩm hot trend", "hàng bán chạy nhất", "bán với giá tốt nhất", "hàng hot hit", "giá sale đặc biệt", "khuyến mại khủng", "quà tặng hấp dẫn", "ưu đãi duy nhất", "giảm giá chớp nhoáng", "deal giá rẻ", "giao hàng tận nơi", "độc quyền giảm giá", "bán hạ giá", "sale siêu khủng", "mua hàng chất lượng", "giảm giá hôm nay", "ưu đãi giờ vàng", "siêu phẩm", "ưu đãi cho khách hàng mới", "siêu ưu đãi", "deal sốc", "mua ngay không chần chừ", "đặc biệt giá tốt", "sản phẩm siêu hot", "xả hàng giá rẻ", "đặt hàng ngay bây giờ", "hàng tồn kho giá rẻ", "mua ngay giá tốt", "khuyến mãi hôm nay", "số lượng hạn chế", "giá hời", "deal cực hời", "ưu đãi giảm giá lớn", "giảm giá lên đến 50%", "siêu sale hôm nay", "giá tốt cho khách hàng mới", "xả kho giá rẻ", "giao hàng siêu nhanh", "ưu đãi giới hạn", "deal khủng hôm nay", "bán tháo hàng", "giảm giá cực mạnh", "siêu khuyến mãi", "chỉ còn vài sản phẩm", "giá rẻ bất ngờ", "mua ngay với giá tốt", "giảm giá hấp dẫn", "sản phẩm giá tốt nhất", "hàng giá rẻ hôm nay", "chỉ có tại hôm nay", "đặc biệt cho hôm nay", "giá cực mềm", "mua ngay kẻo lỡ", "chỉ với hôm nay", "đợt sale lớn", "giảm mạnh chỉ hôm nay", "khuyến mãi hot nhất", "ưu đãi cực lớn", "mua càng nhiều giảm càng sâu", "giao nhanh trong 24h", "giảm giá không giới hạn", "hàng siêu rẻ", "mua sắm thông minh", "giảm giá cực khủng", "deal hot duy nhất hôm nay", "ưu đãi không thể bỏ lỡ", "bán hàng ưu đãi lớn", "bán giá hời", "sản phẩm giá tốt", "siêu giảm giá trong ngày", "giá siêu hời hôm nay", "hàng sale lớn", "deal giá hot nhất", "đặc biệt chỉ hôm nay", "giảm giá trong giờ vàng", "chương trình khuyến mãi sốc", "giảm giá đặc biệt cho khách hàng", "hàng về mới", "khuyến mãi trong ngày", "giá tốt nhất thị trường", "đặt hàng nhanh chóng", "giao hàng nhanh chóng", "chương trình ưu đãi hot", "giảm giá cuối tuần", "ưu đãi không giới hạn", "sản phẩm siêu hot hôm nay", "ưu đãi giá rẻ", "giá cực kỳ ưu đãi", "hàng về liên tục", "giảm mạnh trong hôm nay", "ưu đãi", "miễn phí", "bảo hành", "giá rẻ", "mua ngay", "bán chạy", "hàng đẹp", "giảm sốc", "siêu rẻ", "hàng hot", "mới về", "mẫu mới", "hàng sale", "giá tốt", "giảm giá", "deal hot", "chính hãng", "xả hàng", "ưu tiên", "hàng thật", "khuyến mãi", "siêu hot", "giá sốc", "sản phẩm", "giao nhanh", "giao hàng", "giá ưu", "ưu đãi", "bảo đảm", "mua sắm", "ưu thế", "siêu rẻ", "giảm sâu", "deal sốc", "hàng tồn", "sale khủng", "giảm cực", "mua sớm", "sản phẩm", "khuyến mại", "hàng cao", "deal khủng", "siêu tiết", "giảm mạnh", "ưu đãi", "ưu khủng", "giao miễn", "siêu phẩm", "mua lẻ", "giảm ngay", "hàng chuẩn", "bán tháo", "săn sale", "xả kho", "bảo hành", "bán giá", "chất lượng", "giá ưu", "mua lớn", "siêu tiết", "ưu đãi", "mua liền", "deal hấp", "giảm cực", "sale tốt", "giao tận", "bán hạ", "giá mềm", "ưu tiên", "siêu giảm", "ưu vàng", "giảm khủng", "bán hàng", "giảm hôm", "săn deal", "hàng giảm", "khuyến lớn", "ưu đãi", "mua ngay", "giảm nhẹ", "ưu dịp", "deal hôm", "bán lớn", "giảm duy", "hàng thanh", "deal đỉnh", "hàng chất", "giảm hôm", "bán lẻ", "siêu ưu", "giảm giá", "siêu hời", "ưu đặc", "ưu sale", "giảm sập", "ưu đãi", "deal bất", "giao nhanh", "hàng nhập", "mẫu mới về ", "mẫu mới nhất", "mẫu mới", "hàng chuẩn auth", "hàng chuẩn xịn", "hàng xịn", "xịn đẹp", "hàng công ty ", "hàng cty", "chính hãng"]

def normalized(text):
    # Remove content between emojis and the emojis themselves
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+")

    cleaned_text = re.sub(emoji_pattern.pattern + r'.*?' + emoji_pattern.pattern, '', text).lower()

    # Remove remaining emojis and other special characters
    cleaned_text = ''.join(ch for ch in cleaned_text if unicodedata.category(ch)[0] in ['L', 'N', 'P', 'Z'])

    # Remove characters inside (), [], {}, and other special characters
    pattern = r"\[[^\]]*\]|\([^)]*\)|{[^}]*}|[^\w\s-]"
    cleaned_text = re.sub(pattern, " ", cleaned_text)

    # Remove numbers, adjacent characters, and special characters including cases like FR-91CD
    cleaned_text = re.sub(r'\b[A-Za-z]*\d+[A-Za-z]*\b|\d+|[^\w\s]', ' ', cleaned_text)

    # Remove specific characters:
    cleaned_text = re.sub(r'^\W+|\W+$', ' ', cleaned_text)
        # Xóa các từ vô nghĩa

    for vo_nghia in lst_vo_nghia:
        vo_nghia_normalize = vo_nghia.lower().strip()
        if vo_nghia_normalize in cleaned_text:
            cleaned_text = cleaned_text.replace(vo_nghia_normalize, '').replace('-','').replace('_','')

    # Remove extra whitespace
    cleaned_text = ' '.join(cleaned_text.split())

    if len(cleaned_text) == 0:
        return re.sub(r"\([^)]*\)|{[^}]*}|[^\w\s-]", "", text).lower().strip()
    return cleaned_text.strip().lower()



def extract_list_from_string(string):
    matches = re.search(r'\[(.*?)\]', string, re.DOTALL)
    if matches:
        return eval(matches.group(0))
    else:
        return None


def create_prompt(product_names):
    prompt = """
    Bạn là một chuyên gia về phân loại sản phẩm cho các sản phẩm thương mại điện tử. Tôi sẽ cung cấp cho bạn danh sách các tên sản phẩm thương mại điện tử, mỗi sản phẩm sẽ ở trên một dòng riêng và được đánh số thứ tự.
    
    Kết quả bạn cần đưa ra là các danh mục sản phẩm xuất hiện trong từng tên sản phẩm, tương ứng với mỗi sản phẩm theo thứ tự đã cho.
    
    Các danh mục sản phẩm thường được gọi là “sản phẩm chính” trong tên sản phẩm.
    
    Yêu cầu:
    Với mỗi sản phẩm, bạn phải trích xuất 1 “sản phẩm chính” có trong tên sản phẩm, đảm bảo không bỏ sót bất kỳ sản phẩm nào.
    Nếu bạn xác định được nhiều hơn một “sản phẩm chính”, hãy chọn “sản phẩm chính” có vai trò chính hơn các sản phẩm khác.

    Ví dụ khi gặp tên sản phẩm "Set Nước Thần Keo Ong CNP PROPOLIS TREATMENT AMPULE ESSENCE Làm Đẹp Da Skincare Chăm Sóc Da" thì trả về "nước thần" hoặc khi gặp "Serum MeLa hỗ trợ làm sáng và  và chống tàn nhang, bổ sung và dưỡng ẩm cho da mặt 10ml  Skincare Serum Làm Đẹp Da" thì trả về "serum" hoặc khi gặp tên sản phẩm "Tinh chất dưỡng da trứng cá tầm Vento Luxe (tặng 1 mask)" thì trả về "tinh chất".

    Nếu một sản phẩm không có “sản phẩm chính”, trả về "".
    Khi bạn gặp 1 trường hợp đơn giản chỉ chứa 1 tên sản phẩm chính thì hãy trả về chính nó. Ví dụ như: "Mặt nạ dưỡng ẩm dành cho da" thì trả về "mặt nạ". Hoặc "Bột mặt nạ cho da" thì trả về "bột mặt nạ"    Khi bạn gặp trường hợp có tên sản phẩm combo nhiều sản phẩm khác nhau thì trả về "combo".Ví dụ như: "Combo Dưỡng Da Gel Nha Đam Và Viên Bôi Collagen, Tặng Kèm Gói 100 Mặt Nạ Ủ Tê Skincare Serum", dạng combo này chứa nhiều sản phẩm thì trả về "combo".
    Khi bạn gặp trường hợp có tên sản phẩm có combo cùng 1 sản phẩm thì trả về sản phẩm đó. Ví dụ như: "[COMBO 3] Bobby Tã dán XS70 Siêu khô thoáng Tinh chất gạo non Cho bé" thì trả về "tã dán". hoặc "[Võ Hà Linh x Lucenbase] COMBO 02 chai serum B5B6 30ml" thì trả về "serum".
    Khi bạn gặp trường hợp có tên sản phẩm chính và có cả tên quà tặng thì hãy trả về tên sản phẩm chính. Ví dụ như: "Bộ đôi Sữa rửa mặt dạng gel sạch thoáng dịu nhẹ 120ml & Nước tẩy trang dành cho da dầu m.ụn 400ml - TẶNG 2 Dưỡng chất cho da dầu m.ụn 7.5mlx2" thì trả về "sữa rửa mặt".    Khi bạn gặp trường hợp có tên sản phẩm "Combo 1 ủ trắng lúa mạch collagen 30ml, 1 kem cốt trắng collagen 30gr Sica white tặng 1 serum meso 5ml Hỗ trợ dưỡng trắng hồng da, hỗ trợ cung cấp collagen, hỗ trợ cấp ẩm . Skincare Kem Face Son Massage", trả về "Combo".
    Khi bạn gặp trường hợp chứa rất nhiều tên sản phẩm không cùng loại với nhau thì trả về "combo". Ví dụ như Kem Gạo Mật Ong + Serum Yến [ Tặng Sửa Rửa Mặt 40ml + Chống Nắng 25ml ]" trả về "combo".    Khi bạn gặp trường hợp có tên sản phẩm "Kem dưỡng mặt nạ ngủ Vitamin C & Tinh chất sữa chua" trả về "Combo"
    Trả kết quả dưới dạng một danh sách Python chứa các “sản phẩm chính” trong ngoặc vuông [].
    Mỗi “sản phẩm chính” nên được đặt trong dấu ngoặc kép "" và ngăn cách bởi dấu phẩy.
    Không thêm bất kỳ thông tin nào khác ngoài danh sách.
    Danh sách trả về phải có cùng số lượng phần tử với số lượng sản phẩm mà tôi cung cấp. Ví dụ, tôi cung cấp 5 tên sản phẩm thì phải trả ra chính xác ["product_1","product_2","product_3","product_4","product_5"] hoặc ["product_1","product_2","product_3","","product_5"] nếu có 1 tên sản phẩm không có sản phẩm chính 
    Dưới đây là danh sách sản phẩm:
    """ + "\n".join([f"{i + 1}. {product}" for i, product in enumerate(product_names)])

    return prompt

def payload(promt):
    return json.dumps({
        "messages": [
            {
                "role": "system", 
                "content": "You are an expert in product categorization for e-commerce. Your task is to extract the main product categories from the product name in a consistent and accurate manner. (You are only allowed to extract categories that are present in the product name, and you must not infer or create product categories). You must strictly follow the examples and rules provided. You will only respond with the requested category in the specified format. Be extremely precise and consistent in your classification."
            },
            {
                "role": "user",
                "content": f"{promt}"
            }
        ],
        "model": "openai",
        "seed": 42,
        "temperature": 0.0, # Set to 0 for maximum determinism
        "top-p": 1, # Reduced from 0.5 to be more conservative
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "jsonMode": True
    })


if __name__ == '__main__':
    print("Read_excel")
    file_path = r"/hdd/sv10/svc/docker-svc/jupyter/data/Team_DC/long/API_gpt_4o/get_API_key_raw_example/coffee_update_to_15112024"
    df = pd.read_excel(f"{file_path}.xlsx")
    df = df.sort_values(by="product_name")
    print(df.shape)

    df['product_name_normalized'] = df['product_name'].apply(normalized)
    lst_names = df['product_name_normalized'].tolist()
    lst_keys = df['product_base_id'].tolist()

    batch_size = 10
    jsonl_file_path = f"{file_path}_clean_brand_2.jsonl"

    with open(jsonl_file_path, "w", encoding="utf8") as f:
        for i in tqdm(range(0, len(lst_keys), batch_size), desc="Process", total=len(lst_keys) // batch_size + 1):
            time.sleep(0.5)

            batch_keys = lst_keys[i:i + batch_size]
            batch_names = lst_names[i:i + batch_size]

            prompt = create_prompt(batch_names)
            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=payload(prompt))

            response_json = json.loads(response.text)
            message_content = response_json['choices'][0]['message']['content']

            result = extract_list_from_string(message_content)
            if result is None or len(result) != len(batch_names):
                result = ['no cate'] * len(batch_names)

            for product_id, brand in zip(batch_keys, result):
                json_record = json.dumps({"id": product_id, "brand": brand}, ensure_ascii=False)
                f.write(json_record + "\n")

    print("Done writing JSONL")

    # Convert JSONL to CSV
    csv_file_path = f"{file_path}_clean_cate.csv"

    with open(jsonl_file_path, "r", encoding="utf8") as f:
        data = [json.loads(line) for line in f]

    df_csv = pd.DataFrame(data)
    df_csv.to_csv(csv_file_path, index=False, encoding="utf-8-sig")
    print(f"Successfully written CSV file: {csv_file_path}")
