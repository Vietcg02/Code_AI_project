import requests
import json
import time
import re
import pandas as pd
from tqdm import tqdm

url = "https://text.pollinations.ai/openai"


def normalized(text):
    return str(text).lower().strip().replace("-", " ").replace("_", " ").replace("[", " ").replace("]", " ").replace("\\", " ")




def extract_list_from_string(string):
    matches = re.search(r'\[(.*?)\]', string, re.DOTALL)
    if matches:
        return eval(matches.group(0))
    else:
        return None



    # You are an expert in branding for e-commerce products.
    # I will provide you with a list of e-commerce product names, each product will be on a separate line and numbered. 
    # The result you need to produce is the brand present in each product name, corresponding to each product in the given order.
    # The brand is typically the name of a company, organization, or well-known label. It is usually shorter,does not contain detailed descriptions of the product.

    # Requirements:

    # 1.For each product, you must extract 1 brand include in product name, ensuring that no product is skipped.
    # 2.If you identify more than one brand, select the brand of the main product.
    # 3.Return the result as a Python list containing the brands within square brackets [].
    # 4.Each brand should be enclosed in double quotes "" and separated by commas.
    # 5.If a product does not have a brand, write "no brand".
    # 6.Do not add any additional information other than the list.
    # 7.The returned list must have the same number of elements as the number of products I provide.

    # Below is the list of products:

def create_prompt(product_names):
    prompt = """
    Bạn là một chuyên gia về xây dựng thương hiệu cho các sản phẩm thương mại điện tử.
    Tôi sẽ cung cấp cho bạn một danh sách các tên sản phẩm thương mại điện tử, mỗi sản phẩm sẽ nằm trên một dòng riêng và được đánh số thứ tự.
    Kết quả bạn cần đưa ra là thương hiệu có trong tên của từng sản phẩm, tương ứng với từng sản phẩm theo đúng thứ tự đã cho.
    Thương hiệu thường là tên của công ty, tổ chức, nhãn hiệu nổi tiếng. 

    Yêu cầu:

    Với sản phẩm không có thương hiệu, trả về "no brand".
    Với mỗi sản phẩm, bạn phải trích xuất một thương hiệu có trong tên sản phẩm, đảm bảo không bỏ sót bất kỳ sản phẩm nào.
    Nếu bạn nhận thấy có nhiều hơn một thương hiệu, hãy chọn trả về thương hiệu đúng nhất.
    Nếu trong tên sản phẩm chứa cả sản phẩm tặng kèm thì chỉ lấy thương hiệu của sản phẩm chính mà không lấy thương hiệu từ sản phẩm tặng kèm.
    Trong tên sản phẩm sẽ có rất nhiều thông tin nhiễu (tên shop, ID sản phẩm,..) dễ nhầm lẫn với thương hiệu. Vậy nên nếu không chắc chắn tìm ra được thương hiệu thì hãy trả về "no brand".

    Dưới dây là ví dụ:
    
    <example>
    Sản phẩm: Kem chống nắng Sun Treatment SPF50+ chất kem mềm mịn, dưỡng ẩm, chống nắng cực tốt -Samsam officiall.
    Thương hiệu: Samsam
    Lý do: Thương hiệu là Samsam, những thông tin khác như "Sun Treatment SPF50+" là công dụng không phải thương hiệu
    </example>    
    
    <example>
    Sản phẩm: Kem chống nắng Laroche-posay Effaclar cho da nhạy cảm.
    Thương hiệu: Laroche-posay
    Lý do: Thương hiệu là Laroche-posay, Effaclar là dòng sản phẩm không phải thương hiệu.
    </example>    
    
    <example>
    Sản phẩm: Kem dưỡng da Laroche-posay tặng kèm kem chống nắng Sunplay cho da nhạy cảm.
    Thương hiệu: Laroche-posay
    Lý do: Thương hiệu là Laroche-posay, Sunplay là thương hiệu của sản phẩm tặng kèm nên không lấy.
    </example>    
    
    <example>
    Sản phẩm: Kem Chống Nắng Beplain Kiềm Dầu, Nâng Tông, Cấp Ẩm 50ml Sunscreen SPF50+ PA++++ Hasaki Sản Phẩm Chính Hãng.
    Thương hiệu: Beplain
    Lý do: Thương hiệu là Beplain, Hasaki là tên shop nên không lấy.
    </example>    
    
    <example>
    Sản phẩm: Kem Chống Nắng Beplain Kiềm Dầu, Nâng Tông, Cấp Ẩm 50ml Sunscreen SPF50+ PA++++ Hasaki Sản Phẩm Chính Hãng.
    Thương hiệu: Beplain
    Lý do: Thương hiệu là Beplain, Hasaki là tên shop nên không lấy.
    </example>   
    
    <example>
    Sản phẩm: Kem Chống Nắng Sunplay + Kem dưỡng ẩm Bala.
    Thương hiệu: Sunplay
    Lý do: Thương hiệu là Sunplay,Thương hiệu là Sunplay đúng nhất.
    </example>  
    
    
    
    Output kết quả trả về:
    Chỉ trả về tên thương hiệu theo định dạng array python, yêu cầu không cần giải thích bất cứ điều gì thêm.

    Ví dụ output hợp lệ:
    ["no brand","olay","laroche-posay","olay","obagi","sunplay","beplain","no brand","locknlock","banobagi"]
    """ + "\n".join([f"{i + 1}. {product}" for i, product in enumerate(product_names)])

    return prompt


def payload(promt):
    return json.dumps({
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"{promt}"
            }
        ],
        "model": "openai",
        "seed": 42,
        "jsonMode": True
    })









if __name__ == '__main__':
    print("Read_excel")
    file_path = r"/hdd/sv10/svc/docker-svc/jupyter/data/Team_DC/long/API_gpt_4o/get_API_key_raw_example/tra_update_raw_clean"
    df = pd.read_excel(f"{file_path}.xlsx",sheet_name = "llm")
    df = df.iloc[60_000:]
    print(df.shape)

    lst_names = df['product_name'].apply(normalized).tolist()
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

            try:
                result = extract_list_from_string(message_content)
                if result is None or len(result) != len(batch_names):
                    result = ['no brand'] * len(batch_names)

                for product_id, brand in zip(batch_keys, result):
                    try:
                        # Tạo đối tượng JSON cho mỗi bản ghi
                        json_record = json.dumps({"id": product_id, "brand": brand}, ensure_ascii=False)
                        # Ghi bản ghi vào file JSONL
                        f.write(json_record + "\n")
                    except Exception as e:
                        # Nếu có lỗi khi tạo JSON hoặc ghi file, sẽ in lỗi và tiếp tục với sản phẩm tiếp theo
                        print(f"Error writing record for product_id {product_id}: {e}")
                        continue  # Bỏ qua lỗi và tiếp tục với bản ghi tiếp theo
            except Exception as e:
                # Nếu có lỗi xảy ra trong quá trình trích xuất hoặc xử lý kết quả
                print(f"Error processing batch: {e}")


    print("Done writing JSONL")

    # Convert JSONL to CSV
    csv_file_path = f"{file_path}_clean_brand.csv"

    with open(jsonl_file_path, "r", encoding="utf8") as f:
        data = [json.loads(line) for line in f]

    df_csv = pd.DataFrame(data)
    df_csv.to_csv(csv_file_path, index=False, encoding="utf8")
    print(f"Successfully written CSV file: {csv_file_path}")
