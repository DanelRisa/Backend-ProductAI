import openai
import os


class ChatGPTService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
    
    def get_products_by_dish(self, dish_name:str) -> list[str]:
        prompt = f'хочу приготовить: {dish_name}'
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "напиши список продуктов для приготовления блюда " + prompt + ". Напиши ответ в виде название продукта.  НЕ ИСПОЛЬЗУЙ СВИНИНУ. ВМЕСТО ПШЕНИЧНАЯ МУКА ПИШИ МУКА. Если растительное масло то напиши сразу какой подсолнечное масло или другие виды.Convert answer to JSON format."}

            ],
        max_tokens=9000,
        n=1,
        stop=None,
        temperature=0.0,
        api_key=self.api_key
        )
        
        return completion.choices[0].message.get("content", "")
    
    def get_product_by_category(self, product_name:str) ->str:
        prompt = f'{product_name}'
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "определи в какой из перечисленных категорий относится " + prompt + " исходя из названия продукта и его предназначени: Овощи и фрукты; Напитки и алкогольные напитки; Молоко, сливки, растительное молоко, сгущенное молоко, коктейли молочные; Масло сливочное, спреды, маргарин; Творог, сметана, кефир и кисломолочные продукты; Сыр; Йогурты и творожные сырки; Мука, соль, сахар, приправы, соусы; Яйца; Растительное масло; Кондитерские изделия; Моющие, чистящие средства; Мясо и рыба и птица; Косметика; средства гигиены; Консервы; Снеки; Хлеб и хлебобулочные изделия. Пиши название продукта - категорию. Convert answer to JSON format"},
            ],
            max_tokens=9000,
            n=1,
            stop=None,
            temperature=0.0,
            api_key=self.api_key
        )

        category = completion.choices[0].message.get("content", "")
        
        print("Category:", category)
        return category

 
# {"role": "user", "content": "напиши список продуктов для приготовления блюда " + prompt + " и укажи категорию для каждого продукта исходя из его названия и предназначения. Напиши название продукта, затем черточку (-), затем категорию из следующих: Овощи и фрукты; Напитки и алкогольные напитки; Молоко, сливки, растительное молоко, сгущенное молоко, коктейли молочные; Масло сливочное, спреды, маргарин; Творог, сметана, кефир и кисломолочные продукты; Сыр; Йогурты и творожные сырки; Мука, соль, сахар, приправы, соусы; Яйца; Растительное масло; Кондитерские изделия; Моющие, чистящие средства; Мясо и рыба и птица; Косметика; средства гигиены; Консервы; Снеки; Хлеб и хлебобулочные изделия. Напиши ответ в виде название продукта, категории и ничего лишнего. Если зелень, мясо, специи то сразу уточни какая, не используй слово зелень. Если растительное масло то напиши сразу какой подсолнечное масло или другие виды. Пиши название продукта - категорию. Convert answer to JSON format."}
# {"role": "user", "content": "определи в какой из перечисленных категорий относится " + prompt + " исходя из названия продукта и его предназначени: Овощи и фрукты; Напитки и алкогольные напитки; Молоко, сливки, растительное молоко, сгущенное молоко, коктейли молочные; Масло сливочное, спреды, маргарин; Творог, сметана, кефир и кисломолочные продукты; Сыр; Йогурты и творожные сырки; Мука, соль, сахар, приправы, соусы; Яйца; Растительное масло; Кондитерские изделия; Моющие, чистящие средства; Мясо и рыба и птица; Косметика; средства гигиены; Консервы; Снеки; Хлеб и хлебобулочные изделия . Напиши ответ в виде название продукта, категории и ничего лишнего. Если зелень, мясо, специи то сразу уточни какая, не используй слово зелень. Если растительное масло то напиши сразу какой подсолнечное масло или другие виды. Пиши название продукта - категорию. Convert answer to JSON format"},